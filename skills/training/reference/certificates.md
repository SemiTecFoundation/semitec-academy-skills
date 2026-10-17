# HTML/CSS/JavaScript certificates

Certificate choices are independent: each training may omit its certificate and the package may omit
its certificate. Completion still counts without either. No external approval is required.

Use a dedicated `certificate/` folder containing `index.html`, `index_preview.html`, `certificate.css`,
`certificate.js` and any local assets. The supplied template is editable; there are no prescribed layout
or colour limits. Preview data must be clearly labelled as a non-issued sample.

Reference `"certificate": "certificate/index.html"` in `training.json` (format 1 or 2), or as
`pack.certificate` in a package spec. Academy loads the page in an isolated script-enabled iframe. It
sends `{type: "semitec-certificate", data: {name, training, issuer, date, score, hours, id}}` to the frame.
`date` is ISO and `score` is a fraction or null. `id` is a local completion identifier, not an external
verification registry. Check `event.source === window.parent` and the message type. Apply learner values
with `textContent`; never evaluate received strings. Use a print stylesheet and test A4 landscape output.

For a standalone format-2 page, the author integrates this certificate on its own completion screen
and sends the same data to its iframe. Previewing a design does not earn a credential. Package signatures
verify publisher authenticity and are independent of certificate rendering.

The author-facing final output must always state **certificate: offered/not offered** and provide the
certificate preview path when offered. The packaging output does the same for the package and every
training. Keep legacy `certificate.json` designs when migrating existing material if requested; new
designs should use HTML/CSS/JavaScript.
