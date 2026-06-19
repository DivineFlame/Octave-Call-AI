"""Octave-Call-AI subclass of pipecat's Gemini Live Vertex AI LLM service.

Diamond inheritance: combines the Octave-Call-AI engine-integration overrides from
:class:`OctaveCallAIGeminiLiveLLMService` with the Vertex-specific tweaks from
upstream's :class:`GeminiLiveVertexLLMService` (no history config,
``NON_BLOCKING`` tools disabled, service-account credentials).

MRO::

    OctaveCallAIGeminiLiveVertexLLMService
      -> OctaveCallAIGeminiLiveLLMService
      -> GeminiLiveVertexLLMService
      -> GeminiLiveLLMService
      -> LLMService
      -> ...
"""

from api.services.pipecat.realtime.gemini_live import OctaveCallAIGeminiLiveLLMService
from pipecat.services.google.gemini_live.vertex.llm import (
    GeminiLiveVertexLLMService,
)


class OctaveCallAIGeminiLiveVertexLLMService(
    OctaveCallAIGeminiLiveLLMService,
    GeminiLiveVertexLLMService,
):
    """Vertex AI variant of Gemini Live with Octave-Call-AI integration quirks."""

    pass


# Guard against MRO regressions: a future refactor that flips inheritance
# order or breaks the diamond would silently bypass the Octave-Call-AI overrides.
_mro = OctaveCallAIGeminiLiveVertexLLMService.__mro__
assert _mro[1] is OctaveCallAIGeminiLiveLLMService, (
    f"Expected OctaveCallAIGeminiLiveLLMService at MRO[1], got {_mro[1]}"
)
assert _mro[2] is GeminiLiveVertexLLMService, (
    f"Expected GeminiLiveVertexLLMService at MRO[2], got {_mro[2]}"
)
del _mro
