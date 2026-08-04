from .coevolution import BiologicalPerspective, CoevolutionCarrier, to_potential_gate
from .runtime import ClosureRuntime
from .types import ClosureReceipt, MicroAction, PotentialGate, Resolution, ReturnWitness

__all__ = [
    "BiologicalPerspective",
    "CoevolutionCarrier",
    "to_potential_gate",
    "ClosureRuntime",
    "ClosureReceipt",
    "MicroAction",
    "PotentialGate",
    "Resolution",
    "ReturnWitness",
]

# The closure carrier is intentionally usable without the optional RND/Torch stack.
# When Torch is installed, expose the token-admission adapter as part of the package.
try:
    from .rnd_controller import TokenAdmission, closure_token_admission
except ImportError:  # pragma: no cover - exercised in minimal core installations
    TokenAdmission = None
    closure_token_admission = None
else:
    __all__.extend(["TokenAdmission", "closure_token_admission"])
