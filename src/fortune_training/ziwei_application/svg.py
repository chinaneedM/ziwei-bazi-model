from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Iterable

from fortune_training.calendar_foundation.models import json_value
from fortune_training.util import object_sha256
from fortune_training.ziwei_chart import ChartViewModel


SVG_RENDER_ARTIFACT_SCHEMA = "ZIWEI-TWELVE-PALACE-SVG-ARTIFACT-V1"
SVG_RENDERER_ID = "ZIWEI-TWELVE-PALACE-SVG-RENDERER-V1"
SVG_RENDERER_VERSION = "1.0.0"
SUPPORTED_VIEW_SCHEMA = "ZIWEI-CHART-VIEW-MODEL-V1"

# Conventional Ziwei square-board coordinates inside a 4 x 4 outer ring.
# address_index follows 子=0 ... 亥=11.
PALACE_GRID_COORDINATES: dict[int, tuple[int, int]] = {
    5: (0, 0),  # 巳
    6: (1, 0),  # 午
    7: (2, 0),  # 未
    8: (3, 0),  # 申
    9: (3, 1),  # 酉
    10: (3, 2),  # 戌
    11: (3, 3),  # 亥
    0: (2, 3),  # 子
    1: (1, 3),  # 丑
    2: (0, 3),  # 寅
    3: (0, 2),  # 卯
    4: (0, 1),  # 辰
}


class SvgRenderError(ValueError):
    pass


@dataclass(frozen=True)
class SvgRendererProfile:
    profile_id: str = "ZIWEI-TWELVE-PALACE-SVG-DEFAULT"
    profile_version: str = "1.0.0"
    width: int = 1200
    height: int = 900
    margin: int = 24
    cell_padding: int = 10
    font_family: str = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    header_font_size: int = 16
    body_font_size: int = 12
    metadata_font_size: int = 12
    show_hashes: bool = True
    show_rings: bool = True
    show_temporal: bool = True

    def validate(self) -> "SvgRendererProfile":
        if not self.profile_id.strip() or not self.profile_version.strip():
            raise SvgRenderError("SVG_RENDER_PROFILE_IDENTITY_REQUIRED")
        if not 640 <= self.width <= 4096 or not 480 <= self.height <= 4096:
            raise SvgRenderError("SVG_RENDER_DIMENSIONS_OUT_OF_RANGE")
        if not 0 <= self.margin < min(self.width, self.height) // 4:
            raise SvgRenderError("SVG_RENDER_MARGIN_OUT_OF_RANGE")
        if not 0 <= self.cell_padding <= 64:
            raise SvgRenderError("SVG_RENDER_PADDING_OUT_OF_RANGE")
        for value in (self.header_font_size, self.body_font_size, self.metadata_font_size):
            if not 8 <= value <= 48:
                raise SvgRenderError("SVG_RENDER_FONT_SIZE_OUT_OF_RANGE")
        if not self.font_family.strip() or any(ord(char) < 32 for char in self.font_family):
            raise SvgRenderError("SVG_RENDER_FONT_FAMILY_INVALID")
        return self


@dataclass(frozen=True)
class SvgRenderArtifact:
    renderer_profile: SvgRendererProfile
    source_view_hash: str
    render_hash: str
    svg: str
    schema: str = SVG_RENDER_ARTIFACT_SCHEMA


def _xml(value: object) -> str:
    return escape(str(value), quote=True)


def _short_hash(value: str) -> str:
    return value[:12] if value else "-"


def _chunks(tokens: Iterable[str], *, max_chars: int) -> tuple[str, ...]:
    lines: list[str] = []
    current = ""
    for token in tokens:
        token = str(token)
        candidate = token if not current else f"{current}  {token}"
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = token
        else:
            current = candidate
    if current:
        lines.append(current)
    return tuple(lines)


def _placement_label(row) -> str:
    suffix = ""
    if row.dignity_status == "UNRATED":
        suffix = "[未评级]"
    elif row.dignity_grade:
        suffix = f"[{row.dignity_grade}]"
    badges = "" if not row.transformation_badges else "[" + "|".join(sorted(row.transformation_badges)) + "]"
    return f"{row.label}{suffix}{badges}"


def _canonical_cells(view: ChartViewModel):
    cells = sorted(view.cells, key=lambda row: row.address_index)
    if len(cells) != 12 or {row.address_index for row in cells} != set(range(12)):
        raise SvgRenderError("SVG_RENDER_INVALID_CELL_SET")
    if len({row.branch for row in cells}) != 12:
        raise SvgRenderError("SVG_RENDER_DUPLICATE_BRANCH")
    return tuple(cells)


class ZiweiTwelvePalaceSvgRenderer:
    renderer_id = SVG_RENDERER_ID
    renderer_version = SVG_RENDERER_VERSION
    supported_view_schema = SUPPORTED_VIEW_SCHEMA

    @staticmethod
    def _cell_details(cell, profile: SvgRendererProfile) -> tuple[str, ...]:
        placements = tuple(
            _placement_label(row)
            for row in sorted(cell.placements, key=lambda item: item.entity_id)
        )
        lines: list[str] = list(_chunks(placements, max_chars=30))

        if profile.show_rings and cell.ring_members:
            ring_tokens = tuple(
                row.label
                for row in sorted(cell.ring_members, key=lambda item: (item.ring_id, item.member_id))
            )
            lines.extend("环: " + row for row in _chunks(ring_tokens, max_chars=27))

        if profile.show_temporal:
            temporal_tokens = tuple(
                f"{row.frame_type}:{row.label}"
                for row in sorted(
                    cell.temporal_designations,
                    key=lambda item: (item.frame_type, item.frame_id, item.designation_id),
                )
            )
            lines.extend("时: " + row for row in _chunks(temporal_tokens, max_chars=27))
            if cell.minor_limit_frame_ids:
                lines.extend(
                    "小限: " + row
                    for row in _chunks(tuple(sorted(cell.minor_limit_frame_ids)), max_chars=25)
                )
        return tuple(lines)

    @staticmethod
    def _full_cell_title(cell) -> str:
        placements = ", ".join(
            _placement_label(row)
            for row in sorted(cell.placements, key=lambda item: item.entity_id)
        ) or "-"
        rings = ", ".join(
            row.label
            for row in sorted(cell.ring_members, key=lambda item: (item.ring_id, item.member_id))
        ) or "-"
        temporal = ", ".join(
            f"{row.frame_type}:{row.label}"
            for row in sorted(
                cell.temporal_designations,
                key=lambda item: (item.frame_type, item.frame_id, item.designation_id),
            )
        ) or "-"
        minor = ", ".join(sorted(cell.minor_limit_frame_ids)) or "-"
        return (
            f"{cell.stem}{cell.branch} {cell.natal_designation_label}; "
            f"stars={placements}; rings={rings}; temporal={temporal}; minor={minor}"
        )

    def render(
        self,
        view: ChartViewModel,
        profile: SvgRendererProfile | None = None,
    ) -> SvgRenderArtifact:
        render_profile = (profile or SvgRendererProfile()).validate()
        if view.schema != self.supported_view_schema:
            raise SvgRenderError("SVG_RENDER_VIEW_SCHEMA_MISMATCH")
        if len(view.view_hash) != 64:
            raise SvgRenderError("SVG_RENDER_VIEW_HASH_INVALID")

        cells = _canonical_cells(view)
        width = render_profile.width
        height = render_profile.height
        margin = render_profile.margin
        board_w = width - 2 * margin
        board_h = height - 2 * margin
        cell_w = board_w / 4
        cell_h = board_h / 4

        parts: list[str] = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="chart-title chart-desc" '
                f'font-family="{_xml(render_profile.font_family)}">'
            ),
            '<title id="chart-title">紫微斗数十二宫盘</title>',
            (
                '<desc id="chart-desc">Renderer-neutral Ziwei twelve-palace SVG generated from '
                f'ViewHash {_xml(view.view_hash)}.</desc>'
            ),
            '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>',
        ]

        for cell in cells:
            grid_x, grid_y = PALACE_GRID_COORDINATES[cell.address_index]
            x = margin + grid_x * cell_w
            y = margin + grid_y * cell_h
            title = self._full_cell_title(cell)
            parts.append(
                f'<g id="palace-{cell.address_index}" data-address-index="{cell.address_index}" '
                f'data-branch="{_xml(cell.branch)}">'
            )
            parts.append(f'<title>{_xml(title)}</title>')
            parts.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_w:.2f}" height="{cell_h:.2f}" '
                'fill="#ffffff" stroke="#222222" stroke-width="1"/>'
            )
            header_x = x + render_profile.cell_padding
            header_y = y + render_profile.cell_padding + render_profile.header_font_size
            parts.append(
                f'<text x="{header_x:.2f}" y="{header_y:.2f}" font-size="{render_profile.header_font_size}" '
                'font-weight="700" fill="#111111">'
                f'{_xml(cell.stem)}{_xml(cell.branch)} · {_xml(cell.natal_designation_label)}</text>'
            )

            detail_y = header_y + render_profile.body_font_size + 7
            line_step = render_profile.body_font_size + 4
            for index, line in enumerate(self._cell_details(cell, render_profile)):
                y_pos = detail_y + index * line_step
                if y_pos > y + cell_h - render_profile.cell_padding:
                    break
                parts.append(
                    f'<text x="{header_x:.2f}" y="{y_pos:.2f}" font-size="{render_profile.body_font_size}" '
                    f'fill="#222222">{_xml(line)}</text>'
                )
            parts.append('</g>')

        center_x = margin + cell_w
        center_y = margin + cell_h
        center_w = 2 * cell_w
        center_h = 2 * cell_h
        parts.extend(
            [
                '<g id="chart-center">',
                (
                    f'<rect x="{center_x:.2f}" y="{center_y:.2f}" width="{center_w:.2f}" '
                    f'height="{center_h:.2f}" fill="#fafafa" stroke="#222222" stroke-width="1"/>'
                ),
                (
                    f'<text x="{center_x + 20:.2f}" y="{center_y + 42:.2f}" font-size="24" '
                    'font-weight="700" fill="#111111">紫微斗数</text>'
                ),
                (
                    f'<text x="{center_x + 20:.2f}" y="{center_y + 72:.2f}" '
                    f'font-size="{render_profile.metadata_font_size}" fill="#333333">'
                    f'View: {_xml(view.presentation_profile_id)}@{_xml(view.presentation_profile_version)}</text>'
                ),
            ]
        )
        frames = ", ".join(sorted(view.selected_temporal_frame_ids)) or "NATAL"
        parts.append(
            f'<text x="{center_x + 20:.2f}" y="{center_y + 98:.2f}" '
            f'font-size="{render_profile.metadata_font_size}" fill="#333333">'
            f'Temporal: {_xml(frames)}</text>'
        )
        if render_profile.show_hashes:
            parts.append(
                f'<text x="{center_x + 20:.2f}" y="{center_y + 124:.2f}" '
                f'font-size="{render_profile.metadata_font_size}" fill="#555555">'
                f'FactHash: {_xml(_short_hash(view.source_fact_hash))}</text>'
            )
            parts.append(
                f'<text x="{center_x + 20:.2f}" y="{center_y + 148:.2f}" '
                f'font-size="{render_profile.metadata_font_size}" fill="#555555">'
                f'ViewHash: {_xml(_short_hash(view.view_hash))}</text>'
            )
        parts.extend(['</g>', '</svg>'])
        svg = "\n".join(parts) + "\n"

        render_hash = object_sha256(
            {
                "view_hash": view.view_hash,
                "renderer_profile": json_value(render_profile),
                "renderer": f"{self.renderer_id}@{self.renderer_version}",
                "layout": {str(key): list(value) for key, value in sorted(PALACE_GRID_COORDINATES.items())},
                "svg": svg,
            }
        )
        return SvgRenderArtifact(
            renderer_profile=render_profile,
            source_view_hash=view.view_hash,
            render_hash=render_hash,
            svg=svg,
        )
