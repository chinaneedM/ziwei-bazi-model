from __future__ import annotations

from fortune_training.ziwei_chart.models import Address
from fortune_training.ziwei_chart.registries import address

from .models import AddressOffsetFact


class StructuralTopologyError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def _require_canonical_address(value: Address) -> None:
    canonical = address(value.index)
    if canonical != value:
        raise StructuralTopologyError(
            "NON_CANONICAL_Z12_ADDRESS",
            f"address index/branch mismatch: {value.index}:{value.branch}",
        )


def canonical_addresses() -> tuple[Address, ...]:
    return tuple(address(index) for index in range(12))


def shift(value: Address, offset: int) -> Address:
    _require_canonical_address(value)
    return address(value.index + offset)


def clockwise_offset(source: Address, target: Address) -> int:
    _require_canonical_address(source)
    _require_canonical_address(target)
    return (target.index - source.index) % 12


class NeutralZ12Topology:
    """Generate the complete interpretation-free Z12 address relation matrix."""

    def generate(self) -> tuple[AddressOffsetFact, ...]:
        addresses = canonical_addresses()
        return tuple(
            AddressOffsetFact(
                source=source,
                target=target,
                clockwise_offset=clockwise_offset(source, target),
            )
            for source in addresses
            for target in addresses
        )
