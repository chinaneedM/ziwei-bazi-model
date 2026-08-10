# Ziwei Application V1-R3 — Local Browser App Shell

## Status

```text
LOCAL_APP_ID=ZIWEI-LOCAL-BROWSER-APP-V1
LOCAL_APP_VERSION=1.0.0
APPLICATION_PACKAGE_VERSION=1.2.0
STATUS=CANDIDATE_NOT_ACTIVE
ACTIVATION_CONDITION=MERGED_TO_MAIN
UPSTREAM_APPLICATION=ZIWEI-APPLICATION-V1@1.0.0
UPSTREAM_RENDERER=ZIWEI-TWELVE-PALACE-SVG-RENDERER-V1@1.0.0
ISSUE=#211
```

This slice turns the active Ziwei application/runtime stack into a usable local browser tool. It does not alter calculation, Temporal, Structural R1-R5, canonical source, training, model-learning or prediction contracts.

## Start command

From the repository environment:

```text
fortune-ziwei-app
```

Optional startup controls:

```text
fortune-ziwei-app --port 8765
fortune-ziwei-app --no-browser
fortune-ziwei-app --repository-root /path/to/ziwei-bazi-model
```

The server binds to `127.0.0.1` only. V1 does not expose a command-line option to bind a public interface.

## Public local path

```text
Browser form
-> POST /api/resolve
-> LocalZiweiApplication
-> BirthInput
-> active V1 calculation profile
-> ApplicationBirthRequest
-> ZiweiChartService.resolve()
-> ApplicationChartBundle
-> application export
-> ZiweiTwelvePalaceSvgRenderer
-> browser SVG result
```

The HTTP/UI layer does not reimplement Time/Calendar, placement, Temporal, Structural or renderer rules.

## Input scope

The first local form exposes:

- Gregorian local birth datetime;
- birth-place label;
- latitude / longitude;
- IANA timezone id;
- sex;
- optional Daxian frame id;
- optional Annual year;
- optional Minor-Limit age.

The active CalculationProfile is built from current repository configuration. The user does not manually construct a profile object.

No geocoding or timezone network service is used in R3. Coordinates and timezone remain explicit inputs.

## Local endpoints

```text
GET  /            fixed application HTML
GET  /style.css   fixed local CSS
GET  /app.js      fixed local JavaScript
GET  /health      versioned health JSON
POST /api/resolve versioned chart resolve JSON
```

There is no arbitrary file-read/write endpoint and no command-execution endpoint.

SVG and JSON downloads are created client-side from the already-returned deterministic response, so the browser never supplies a server filesystem path.

## Resolve response

`POST /api/resolve` returns:

```text
ZIWEI-LOCAL-APP-RESOLVE-V1
├── application_export
├── svg_artifact metadata
│   ├── source ViewHash
│   └── RenderHash
└── standalone SVG string
```

The response does not serialize all private runtime objects. It stays on the existing application export and renderer boundaries.

## Error boundary

Local input failures return a stable error envelope:

```text
ZIWEI-LOCAL-APP-ERROR-V1
└── error
    ├── code
    └── detail
```

Application/runtime diagnostic codes are preserved where available.

## Security boundary

R3 is deliberately local-only:

- bind address is frozen to `127.0.0.1`;
- no public bind option;
- no external HTTP calls;
- no telemetry;
- no cloud persistence;
- no account/auth layer;
- request body limit is 64 KiB;
- `/api/resolve` requires `application/json`;
- malformed UTF-8/JSON is rejected;
- timezone is validated through the local IANA/tzdata registry;
- HTML/CSS/JS assets are fixed application constants, not user templates;
- page uses a restrictive Content-Security-Policy;
- SVG renderer retains its XML escaping / no-script / no-remote-asset contract;
- browser output uses text-safe DOM APIs for status/error fields;
- no arbitrary server-side filesystem download path exists.

## UI scope

The first UI is intentionally functional rather than final:

- desktop-first input grid;
- deterministic twelve-palace SVG result;
- resolution status;
- abbreviated BundleHash / ViewHash / RenderHash;
- client-side SVG download;
- client-side JSON download;
- no prediction or interpretation panel.

Visual styling is not a calculation correctness signal. Wenmo acceptance remains tracked separately in Issue #208.

## Candidate validation gate

Before activation the exact merge-candidate head must pass:

- server binds to `127.0.0.1` on an ephemeral test port;
- `/health` returns fixed versioned status and security headers;
- local HTML/CSS/JS have no external HTTP dependencies;
- real HTTP fixture `1994-05-17 14:30 Beijing male` resolves successfully;
- application ViewHash equals SVG artifact source ViewHash;
- BundleHash / RenderHash are valid deterministic identities;
- local response and application export schemas validate;
- same HTTP request reproduces BundleHash / ViewHash / RenderHash / SVG exactly;
- invalid sex/timezone/datetime/numeric input returns structured 4xx;
- malformed, oversized and wrong-content-type requests are rejected;
- user-supplied HTML in birth-place text is not reflected as executable SVG/HTML;
- repository bootstrap PASS;
- `fortune-train verify` PASS;
- full unittest PASS;
- branch behind=0;
- diff audit confirms no Foundation/canonical/training/model-learning/prediction mutation.

## Post-R3

After activation the repository will contain an actually operable local Ziwei chart application shell. The next priority should not be another large architecture layer.

Two bounded follow-ups remain:

1. complete external Wenmo acceptance #208 when the reference screenshot/text is supplied;
2. refine real-use UX (location presets/history/visual details) only after using the local app, without changing frozen calculation contracts.
