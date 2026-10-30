# Autoresearch methodology reference

Source: https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117
Pinned revision: `228791fb499afffb54b46200aca536f79142f117`.

The upstream project experiments on single-GPU language-model training. It fixes
the evaluation/data preparation, changes the candidate training code, measures
validation bits per byte, and records which trials improve the result. Its
documented setup uses an NVIDIA GPU, Python 3.10+, uv and training dependencies.
Those dependencies, datasets, notebooks and model-training runtime are not vendored
or installed here. This library stores the reference and a bounded team adaptation.

Use `skills/research/bounded-agent-research` and
`prompts/teams/bounded-research.md` for explicitly budgeted experiments. Preserve
immutable evaluation, isolated trials and complete results. Do not inherit the
upstream unbounded loop, disabled-permission suggestion, or destructive reset
workflow. Installing this library does not authorize a GPU job or service spend.

License evidence: the pinned README declares MIT. The reviewed tree has no
standalone LICENSE file. See LICENSE-NOTICE.md; no upstream runtime code is copied.
