from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256

from .integrity import HashBundle, validate_natal_chart, validate_temporal_state
from .models import NatalChartState
from .registries import address
from .temporal import AnnualFrame, DaxianFrame, MinorLimitFrame, MonthlyFrame, TemporalNatalContext, ZiweiTemporalState


VIEW_PROJECTION_ALGORITHM_ID = "ZIWEI-VIEW-PROJECTION-V1"
VIEW_PROJECTION_ALGORITHM_VERSION = "1.0.3"
TEXT_RENDERER_ID = "ZIWEI-PLAIN-TEXT-RENDERER-V1"
TEXT_RENDERER_VERSION = "1.0.3"


class ViewProjectionError(ValueError):
    pass


@dataclass(frozen=True)
class LexemeOverride:
    namespace: str
    object_id: str
    label: str


@dataclass(frozen=True)
class PresentationProfile:
    profile_id: str
    profile_version: str
    address_order: str = "BRANCH_FORWARD"
    show_dignity: bool = True
    show_transformations: bool = True
    show_rings: bool = True
    show_roles: bool = True
    show_temporal_overlays: bool = True
    lexeme_overrides: tuple[LexemeOverride, ...] = ()

    def validate(self) -> "PresentationProfile":
        if not self.profile_id.strip() or not self.profile_version.strip():
            raise ViewProjectionError("VIEW_PROFILE_IDENTITY_REQUIRED")
        if self.address_order not in {"BRANCH_FORWARD", "LIFE_FIRST_FORWARD"}:
            raise ViewProjectionError("VIEW_UNSUPPORTED_ADDRESS_ORDER")
        keys = [(row.namespace, row.object_id) for row in self.lexeme_overrides]
        if len(keys) != len(set(keys)):
            raise ViewProjectionError("VIEW_DUPLICATE_LEXEME_OVERRIDE")
        if any(not row.label.strip() for row in self.lexeme_overrides):
            raise ViewProjectionError("VIEW_EMPTY_LEXEME_OVERRIDE")
        return self


@dataclass(frozen=True)
class ViewPlacement:
    entity_id: str
    label: str
    dignity_grade: str | None
    transformation_badges: tuple[str, ...]
    dignity_status: str | None = None


@dataclass(frozen=True)
class ViewRingMember:
    ring_id: str
    member_id: str
    label: str


@dataclass(frozen=True)
class ViewDesignationOverlay:
    frame_type: str
    frame_id: str
    designation_id: str
    label: str


@dataclass(frozen=True)
class ViewTemporalAuxiliary:
    frame_type: str
    frame_id: str
    entity_id: str
    label: str


@dataclass(frozen=True)
class ViewRole:
    role_id: str
    label: str
    entity_id: str
    entity_label: str


@dataclass(frozen=True)
class PalaceViewCell:
    address_index: int
    branch: str
    stem: str
    natal_designation_id: str
    natal_designation_label: str
    placements: tuple[ViewPlacement, ...]
    ring_members: tuple[ViewRingMember, ...]
    temporal_designations: tuple[ViewDesignationOverlay, ...]
    temporal_auxiliaries: tuple[ViewTemporalAuxiliary, ...]
    minor_limit_frame_ids: tuple[str, ...]
    doujun_frame_ids: tuple[str, ...]


@dataclass(frozen=True)
class ChartViewModel:
    schema: str
    presentation_profile_id: str
    presentation_profile_version: str
    source_fact_hash: str
    source_computation_hash: str
    selected_temporal_frame_ids: tuple[str, ...]
    roles: tuple[ViewRole, ...]
    cells: tuple[PalaceViewCell, ...]
    view_hash: str


class ZiweiViewProjectionCompiler:
    schema = "ZIWEI-CHART-VIEW-MODEL-V1"

    @staticmethod
    def _override_map(profile: PresentationProfile) -> dict[tuple[str, str], str]:
        return {(row.namespace, row.object_id): row.label for row in profile.lexeme_overrides}

    @staticmethod
    def _label(overrides: dict[tuple[str, str], str], namespace: str, object_id: str, fallback: str) -> str:
        return overrides.get((namespace, object_id), fallback)

    @staticmethod
    def _select_daxian(state: ZiweiTemporalState | None, frame_id: str | None) -> DaxianFrame | None:
        if frame_id is None:
            return None
        if state is None:
            raise ViewProjectionError("VIEW_TEMPORAL_STATE_REQUIRED")
        rows = [row for row in state.daxian_frames if row.frame_id == frame_id]
        if len(rows) != 1:
            raise ViewProjectionError("VIEW_DAXIAN_FRAME_NOT_FOUND")
        return rows[0]

    @staticmethod
    def _select_annual(state: ZiweiTemporalState | None, year: int | None) -> AnnualFrame | None:
        if year is None:
            return None
        if state is None:
            raise ViewProjectionError("VIEW_TEMPORAL_STATE_REQUIRED")
        rows = [row for row in state.annual_frames if row.absolute_year == year]
        if len(rows) != 1:
            raise ViewProjectionError("VIEW_ANNUAL_FRAME_NOT_FOUND")
        return rows[0]

    @staticmethod
    def _select_minor(state: ZiweiTemporalState | None, age: int | None) -> MinorLimitFrame | None:
        if age is None:
            return None
        if state is None:
            raise ViewProjectionError("VIEW_TEMPORAL_STATE_REQUIRED")
        rows = [row for row in state.minor_limit_frames if row.nominal_age == age]
        if len(rows) != 1:
            raise ViewProjectionError("VIEW_MINOR_LIMIT_FRAME_NOT_FOUND")
        return rows[0]

    @staticmethod
    def _select_monthly(
        state: ZiweiTemporalState | None,
        annual_year: int | None,
        lunar_month: int | None,
    ) -> MonthlyFrame | None:
        if lunar_month is None:
            return None
        if annual_year is None:
            raise ViewProjectionError("VIEW_MONTH_REQUIRES_ANNUAL_YEAR")
        if state is None:
            raise ViewProjectionError("VIEW_TEMPORAL_STATE_REQUIRED")
        rows = [
            row
            for row in state.monthly_frames
            if row.absolute_year == annual_year and row.lunar_month == lunar_month
        ]
        if len(rows) != 1:
            raise ViewProjectionError("VIEW_MONTHLY_FRAME_NOT_FOUND")
        return rows[0]

    @staticmethod
    def _view_payload(model: ChartViewModel) -> dict:
        payload = json_value(model)
        payload.pop("view_hash", None)
        return payload

    @staticmethod
    def _placement_identity(rows) -> tuple[tuple[str, int], ...]:
        return tuple(sorted((row.entity_id, row.address.index) for row in rows))

    def compile(
        self,
        chart: NatalChartState,
        hashes: HashBundle,
        presentation: PresentationProfile,
        *,
        temporal_state: ZiweiTemporalState | None = None,
        temporal_context: TemporalNatalContext | None = None,
        daxian_frame_id: str | None = None,
        annual_year: int | None = None,
        lunar_month: int | None = None,
        minor_limit_age: int | None = None,
    ) -> ChartViewModel:
        presentation.validate()
        natal_integrity = validate_natal_chart(chart)
        if natal_integrity.status != "PASS":
            raise ViewProjectionError("VIEW_SOURCE_NATAL_INTEGRITY_FAILED")

        if temporal_state is not None:
            if temporal_context is None:
                raise ViewProjectionError("VIEW_TEMPORAL_CONTEXT_REQUIRED")
            if self._placement_identity(temporal_context.placements) != self._placement_identity(chart.placements):
                raise ViewProjectionError("VIEW_TEMPORAL_CONTEXT_CHART_MISMATCH")
            temporal_integrity = validate_temporal_state(temporal_state, temporal_context)
            if temporal_integrity.status != "PASS":
                raise ViewProjectionError("VIEW_SOURCE_TEMPORAL_INTEGRITY_FAILED")
        elif temporal_context is not None:
            raise ViewProjectionError("VIEW_TEMPORAL_STATE_REQUIRED")

        overrides = self._override_map(presentation)
        daxian = self._select_daxian(temporal_state, daxian_frame_id)
        annual = self._select_annual(temporal_state, annual_year)
        monthly = self._select_monthly(temporal_state, annual_year, lunar_month)
        minor = self._select_minor(temporal_state, minor_limit_age)
        selected_frames = tuple(row.frame_id for row in (daxian, annual, monthly, minor) if row is not None)

        stem_by_address = {row.address.index: row.stem for row in chart.structure.address_attributes}
        natal_designation_by_address = {row.address.index: row for row in chart.structure.designation_bindings}
        dignity_by_entity = {
            row.target_entity_id: row
            for row in chart.annotations
            if row.annotation_type == "DIGNITY"
        }

        transformation_by_entity: dict[str, list[str]] = {}
        if presentation.show_transformations:
            activation_sets: list[Iterable] = [chart.transformations]
            if daxian is not None:
                activation_sets.append(daxian.transformations)
            if annual is not None:
                activation_sets.append(annual.transformations)
            if monthly is not None:
                activation_sets.append(monthly.transformations)
            for rows in activation_sets:
                for row in rows:
                    transformation_by_entity.setdefault(row.target_entity_id, []).append(
                        f"{row.source_layer}:{row.transformation_type}"
                    )

        placements_by_address: dict[int, list[ViewPlacement]] = {index: [] for index in range(12)}
        for row in chart.placements:
            dignity = dignity_by_entity.get(row.entity_id) if presentation.show_dignity else None
            placements_by_address[row.address.index].append(
                ViewPlacement(
                    entity_id=row.entity_id,
                    label=self._label(overrides, "ENTITY", row.entity_id, row.display_name),
                    dignity_grade=dignity.grade if dignity is not None else None,
                    transformation_badges=tuple(sorted(transformation_by_entity.get(row.entity_id, ()))),
                    dignity_status=dignity.status if dignity is not None else None,
                )
            )
        for rows in placements_by_address.values():
            rows.sort(key=lambda item: item.entity_id)

        ring_by_address: dict[int, list[ViewRingMember]] = {index: [] for index in range(12)}
        if presentation.show_rings:
            for ring in chart.rings:
                for member in ring.members:
                    ring_by_address[member.address.index].append(
                        ViewRingMember(
                            ring_id=ring.ring_id,
                            member_id=member.member_id,
                            label=self._label(overrides, "RING_MEMBER", member.member_id, member.display_name),
                        )
                    )
        for rows in ring_by_address.values():
            rows.sort(key=lambda item: (item.ring_id, item.member_id))

        overlays_by_address: dict[int, list[ViewDesignationOverlay]] = {index: [] for index in range(12)}
        auxiliaries_by_address: dict[int, list[ViewTemporalAuxiliary]] = {index: [] for index in range(12)}
        if presentation.show_temporal_overlays:
            for frame_type, frame in (("DAXIAN", daxian), ("ANNUAL", annual), ("MONTH", monthly)):
                if frame is None:
                    continue
                for row in frame.designation_overlay:
                    overlays_by_address[row.address.index].append(
                        ViewDesignationOverlay(
                            frame_type=frame_type,
                            frame_id=frame.frame_id,
                            designation_id=row.designation_id,
                            label=self._label(overrides, "DESIGNATION", row.designation_id, row.display_name),
                        )
                    )
                for row in frame.auxiliary_activations:
                    auxiliaries_by_address[row.target_address.index].append(
                        ViewTemporalAuxiliary(
                            frame_type=frame_type,
                            frame_id=frame.frame_id,
                            entity_id=row.entity_id,
                            label=self._label(overrides, "ENTITY", row.entity_id, row.display_name),
                        )
                    )

        minor_by_address: dict[int, list[str]] = {index: [] for index in range(12)}
        if presentation.show_temporal_overlays and minor is not None:
            minor_by_address[minor.active_address.index].append(minor.frame_id)

        doujun_by_address: dict[int, list[str]] = {index: [] for index in range(12)}
        if presentation.show_temporal_overlays and annual is not None:
            doujun_by_address[annual.doujun_address.index].append(annual.frame_id)

        roles: list[ViewRole] = []
        if presentation.show_roles:
            for row in chart.role_bindings:
                roles.append(
                    ViewRole(
                        role_id=row.role_id,
                        label=self._label(overrides, "ROLE", row.role_id, row.display_name),
                        entity_id=row.entity_id,
                        entity_label=self._label(overrides, "ENTITY", row.entity_id, row.entity_display_name),
                    )
                )
            roles.sort(key=lambda item: item.role_id)

        if presentation.address_order == "BRANCH_FORWARD":
            order = list(range(12))
        else:
            start = chart.structure.life_address.index
            order = [(start + offset) % 12 for offset in range(12)]

        cells: list[PalaceViewCell] = []
        for index in order:
            designation = natal_designation_by_address[index]
            cells.append(
                PalaceViewCell(
                    address_index=index,
                    branch=address(index).branch,
                    stem=stem_by_address[index],
                    natal_designation_id=designation.designation_id,
                    natal_designation_label=self._label(
                        overrides, "DESIGNATION", designation.designation_id, designation.display_name
                    ),
                    placements=tuple(placements_by_address[index]),
                    ring_members=tuple(ring_by_address[index]),
                    temporal_designations=tuple(overlays_by_address[index]),
                    temporal_auxiliaries=tuple(
                        sorted(
                            auxiliaries_by_address[index],
                            key=lambda item: (item.frame_type, item.frame_id, item.entity_id),
                        )
                    ),
                    minor_limit_frame_ids=tuple(minor_by_address[index]),
                    doujun_frame_ids=tuple(doujun_by_address[index]),
                )
            )

        provisional = ChartViewModel(
            schema=self.schema,
            presentation_profile_id=presentation.profile_id,
            presentation_profile_version=presentation.profile_version,
            source_fact_hash=hashes.fact_hash,
            source_computation_hash=hashes.computation_hash,
            selected_temporal_frame_ids=selected_frames,
            roles=tuple(roles),
            cells=tuple(cells),
            view_hash="",
        )
        view_hash = object_sha256(
            {
                "presentation_profile": json_value(presentation),
                "view_payload": self._view_payload(provisional),
                "projection_algorithm": f"{VIEW_PROJECTION_ALGORITHM_ID}@{VIEW_PROJECTION_ALGORITHM_VERSION}",
            }
        )
        return replace(provisional, view_hash=view_hash)


class PlainTextZiweiRenderer:
    renderer_id = TEXT_RENDERER_ID
    renderer_version = TEXT_RENDERER_VERSION
    supported_view_schema = ZiweiViewProjectionCompiler.schema

    @staticmethod
    def _dignity_suffix(row: ViewPlacement) -> str:
        if row.dignity_status == "UNRATED":
            return "[未评级]"
        return f"[{row.dignity_grade}]" if row.dignity_grade else ""

    def render(self, view: ChartViewModel) -> str:
        if view.schema != self.supported_view_schema:
            raise ViewProjectionError("VIEW_RENDERER_SCHEMA_MISMATCH")
        lines = [
            f"view={view.presentation_profile_id}@{view.presentation_profile_version}",
            f"fact_hash={view.source_fact_hash}",
            f"computation_hash={view.source_computation_hash}",
            f"view_hash={view.view_hash}",
        ]
        if view.roles:
            lines.append("roles=" + ", ".join(f"{row.label}:{row.entity_label}" for row in view.roles))
        for cell in view.cells:
            stars = ", ".join(
                row.label
                + self._dignity_suffix(row)
                + (f"[{'|'.join(row.transformation_badges)}]" if row.transformation_badges else "")
                for row in cell.placements
            ) or "-"
            rings = ", ".join(row.label for row in cell.ring_members) or "-"
            temporal = ", ".join(f"{row.frame_type}:{row.label}" for row in cell.temporal_designations)
            if cell.temporal_auxiliaries:
                moving = ", ".join(
                    f"{row.frame_type}:{row.label}" for row in cell.temporal_auxiliaries
                )
                temporal = ", ".join(filter(None, (temporal, moving)))
            if cell.minor_limit_frame_ids:
                temporal = ", ".join(filter(None, (temporal, "小限:" + "/".join(cell.minor_limit_frame_ids))))
            if cell.doujun_frame_ids:
                temporal = ", ".join(filter(None, (temporal, "斗君:" + "/".join(cell.doujun_frame_ids))))
            temporal = temporal or "-"
            lines.append(
                f"{cell.stem}{cell.branch} {cell.natal_designation_label} | stars={stars} | rings={rings} | temporal={temporal}"
            )
        return "\n".join(lines)
