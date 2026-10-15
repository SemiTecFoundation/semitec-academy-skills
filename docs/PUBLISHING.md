# Open authoring and publishing

Academy Templates has two paths. An author may create a lab, interactive training or project and use it
standalone. Packaging is optional: it copies selected materials into one `.stlp` archive for SemiTec
Academy. Neither path needs a partner agreement or SemiTec Foundation approval.

```text
author → standalone material → technical check → publisher metadata → optional certificate + signing
       → package / catalog → recipient chooses to trust publisher key → Academy
```

`stlp check` is a technical gate: fix every error before a package is shared. It is not editorial or
institutional approval. The publisher should make its own short review of accuracy, citations, rights,
learner suitability and included files.

For a package, identify the responsible `publisher` and `authors`, and optionally provide a `contact`
object for feedback. Add `certificate` only when that publisher intends to issue a local course-completion
record; omitting it creates a perfectly valid package without a course certificate. Do not call a
publisher certificate “SemiTec Foundation certified” unless the Foundation actually issued it.

Partners sign releases with their own Ed25519 private key and distribute only their `.stlp`, public key
and fingerprint. A school or user adds that public key in Academy's *Settings → Application → Trusted
publishers*. Trust is the recipient's decision, not a central approval queue. Unsigned packages are for
the author’s local Developer-mode test only.

The skills and templates are [Apache-2.0](../LICENSE). Authors and publishers keep responsibility for
the content they create, its content license, third-party permissions and attribution. See
[TRADEMARKS.md](../TRADEMARKS.md) before using SemiTec names or logos.
