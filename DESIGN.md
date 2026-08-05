---
name: Southern San Andreas Autos
description: Um marketplace de carros lido como painel de instrumentos à noite — chapa escura, fios de 1px, âmbar só onde haveria luz.
colors:
  ink-950: "#080A0D"
  ink-900: "#0F1216"
  ink-800: "#14181E"
  ink-700: "#1A1F27"
  ink-600: "#232935"
  ink-500: "#2E3542"
  ink-400: "#3C4552"
  slate-500: "#5E6878"
  slate-400: "#7B8595"
  slate-300: "#9BA5B4"
  slate-200: "#C3CAD5"
  slate-100: "#E4E8EE"
  white: "#F5F7FA"
  amber-600: "#B98A1C"
  amber-500: "#E8B33A"
  amber-400: "#F4C866"
  amber-300: "#FBDD9B"
  amber-glow: "rgba(232, 179, 58, 0.16)"
  amber-wash: "rgba(232, 179, 58, 0.07)"
  signal-go: "#38C172"
  signal-go-hi: "#45D482"
  signal-go-ink: "#06210F"
  signal-go-wash: "rgba(56, 193, 114, 0.12)"
  signal-stop: "#E5484D"
  signal-stop-wash: "rgba(229, 72, 77, 0.12)"
  signal-warn: "#E8913A"
  signal-warn-wash: "rgba(232, 145, 58, 0.12)"
  scrim: "rgba(8, 10, 13, 0.72)"
  scrim-strong: "rgba(8, 10, 13, 0.82)"
typography:
  display:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "3.5rem"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.02em"
    fontVariation: "font-stretch: 90%"
  headline:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.015em"
    fontVariation: "font-stretch: 92%"
  title:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  subtitle:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontVariation: "font-stretch: 92%"
  lead:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.2
    fontVariation: "font-stretch: 96%"
  body:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  small:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Archivo, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontSize: "0.6875rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.14em"
    fontVariation: "font-stretch: 88%"
rounded:
  sm: "2px"
  md: "3px"
  lg: "4px"
  pill: "999px"
spacing:
  s1: "0.25rem"
  s2: "0.5rem"
  s3: "0.75rem"
  s4: "1rem"
  s5: "1.5rem"
  s6: "2rem"
  s7: "3rem"
  s8: "4rem"
components:
  button-primary:
    backgroundColor: "{colors.amber-500}"
    textColor: "{colors.ink-950}"
    rounded: "{rounded.md}"
    padding: "0.75rem 1.5rem"
    typography: "{typography.small}"
  button-primary-hover:
    backgroundColor: "{colors.amber-400}"
    textColor: "{colors.ink-950}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.slate-200}"
    rounded: "{rounded.md}"
    padding: "0.75rem 1.5rem"
  button-ghost-hover:
    textColor: "{colors.white}"
  button-go:
    backgroundColor: "{colors.signal-go}"
    textColor: "{colors.signal-go-ink}"
    rounded: "{rounded.md}"
    padding: "1rem 2rem"
    typography: "{typography.body}"
  button-danger:
    backgroundColor: "transparent"
    textColor: "{colors.signal-stop}"
    rounded: "{rounded.md}"
    padding: "0.75rem 1.5rem"
  card:
    backgroundColor: "{colors.ink-800}"
    rounded: "{rounded.lg}"
    padding: "1rem"
  panel:
    backgroundColor: "{colors.ink-800}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  input:
    backgroundColor: "{colors.ink-700}"
    textColor: "{colors.slate-100}"
    rounded: "{rounded.md}"
    padding: "0.75rem"
  chip:
    backgroundColor: "{colors.amber-wash}"
    textColor: "{colors.amber-300}"
    rounded: "{rounded.sm}"
    padding: "0.25rem 0.75rem"
    typography: "{typography.small}"
  tag:
    backgroundColor: "{colors.ink-950}"
    textColor: "{colors.signal-go}"
    rounded: "{rounded.sm}"
    padding: "3px 0.5rem"
    typography: "{typography.label}"
  navlink:
    backgroundColor: "transparent"
    textColor: "{colors.slate-300}"
    rounded: "{rounded.md}"
    padding: "0.5rem 0.75rem"
    typography: "{typography.small}"
  navlink-primary:
    backgroundColor: "{colors.amber-500}"
    textColor: "{colors.ink-950}"
    rounded: "{rounded.md}"
    padding: "0.5rem 0.75rem"
---

# Design System: Southern San Andreas Autos

## Overview

**Creative North Star: "The Night Dashboard"**

The whole product reads as an instrument cluster seen at night, not as a bright classifieds grid. The page floor is a near-black steel (`#0F1216`); panels are a slightly lighter plate stacked on it; every division is a 1px hairline. Amber is not decorative gold — it is dial backlighting, and it appears only where a real gauge would emit light: the price, the active filter, the rule under a section title. The second material is the magazine spec sheet: label/value pairs on hairlines, tabular numerals everywhere, four-column datasheets that close in exact rows.

The world was chosen against two defaults at once. It refuses the white-and-blue marketplace grid the category always ships, and it equally refuses "dark premium with glowing gold," which is the predictable opposite. What keeps it from landing in either is the material derivation: the tick rule (a speedometer scale drawn in two repeating gradients), the amber-as-backlight discipline, and a single variable typeface whose width axis does the gauge lettering.

Density is high and deliberate. The buyer scans price and photo, narrows by transmission/fuel/price band, opens the spec sheet, and leaves for the seller's WhatsApp. Every surface is tuned for that scan: the price is the brightest thing in a card, the result count is set at headline size, and nothing decorative competes with either.

**Key Characteristics:**
- Near-black steel ground with plate-on-plate panels, never a light surface
- Amber (`#E8B33A`) reserved for emitted light: price, active filter, section rules
- 1px hairlines instead of shadows; the system is unlit-flat by default
- Corners of 2–4px; nothing rounded except circular counters
- One variable typeface (Archivo) whose `wdth` axis makes the gauge lettering
- Tick rules as the recurring motif that divides sections
- Tabular numerals globally; numbers are readings, not text

## Colors

A single-accent instrument palette: seven steps of blue-black steel, six steps of cool slate for text, amber as the only light source, and a small signal set borrowed from dashboard warning lamps.

### Primary
- **Dial Amber** (`#E8B33A`): the backlight. Price readings, the lit tick rule under the price, active-nav state, focus outlines, filter-active borders, section titles, required-field asterisks, the seller-entry CTA. It is the highest-value pixel on any screen and must stay scarce.
- **Amber Filament** (`#F4C866`): hover brightening of any amber surface; the seminovo tag's text.
- **Amber Ember** (`#B98A1C`): the dimmed amber used for borders and hairlines that should read as amber without emitting — chip borders, filled-filter borders, the price readout's frame, the finer graduation of a lit rule.
- **Amber Halo** (`#FBDD9B`) and the two translucent films, **Amber Glow** (16% amber) and **Amber Wash** (7% amber): chip text, radial bloom above the price readout, and the faint fill behind a filled filter field.

### Secondary
- **Signal Go** (`#38C172`): the dashboard's green lamp. Two jobs only — the `Novo` condition tag and the WhatsApp contact button, which is the one action the whole product exists to produce. Its dark counter-ink (`#06210F`) is what sits on top of it.

### Tertiary
- **Signal Stop** (`#E5484D`) and **Signal Warn** (`#E8913A`): warning lamps. Field errors, error alerts, destructive buttons, warning alerts. Never used for emphasis or decoration.

### Neutral
- **Well Black** (`#080A0D`): the pit behind everything — masthead, footer, image frames, tag backgrounds, and the ink that sits on amber surfaces.
- **Floor** (`#0F1216`): the page ground. Every screen starts here.
- **Plate** (`#14181E`): panels, cards, the filter rail, datasheet cells.
- **Raised Plate** (`#1A1F27`): form fields and inset controls — inputs sit *above* the panel, not carved into it.
- **Heavy Hairline** (`#232935`): panel borders and weight dividers.
- **Hairline** (`#2E3542`): the default 1px stroke — field borders, ghost buttons, dashed drop zones.
- **Graduation** (`#3C4552`): the fine tick strokes on a rule, the `·` separators in data lines, and the hover border of a card.
- **Disabled Slate** (`#5E6878`): disabled text and absent-value states only.
- **Meta Slate** (`#7B8595`): gauge labels, spec keys, meta lines, currency marks.
- **Secondary Slate** (`#9BA5B4`): secondary body copy, placeholders, help text, nav links at rest.
- **Body Slate** (`#C3CAD5`): default body text on the floor.
- **Strong Body** (`#E4E8EE`): spec values, field input text, alert copy.
- **Readout White** (`#F5F7FA`): headings, card names, datasheet values, result counts.

### Named Rules
**The Backlight Rule.** Amber marks emitted light, never surface decoration. A thing may be amber only if it is a reading (a price), an active indicator (a filled filter, the current nav item, focus), or the rule that sits under a title. Two sanctioned exceptions exist and no third one is granted: the masthead `Anunciar carro` button stays filled amber because it is the seller's single entry into the product, and the rail's apply button fills amber only once the filter form is dirty (`data-dirty="true"`). If a new amber surface is neither of those, it is wrong.

**The Disabled-Slate Rule.** `#5E6878` is reserved for disabled text and absent values. It fails contrast as body copy — placeholders, help text, and secondary prose use `#9BA5B4` or lighter. This is a hard floor, not a preference.

**The Pinned Ground Rule.** `#0F1216`, `#E8B33A` and `#38C172` are user-pinned and binding. They are not derived from a formula and are not open to re-derivation; new tones extend the existing ink/slate/amber ramps rather than introducing new hues.

## Typography

**Single Family:** Archivo Variable (with `ui-sans-serif, system-ui, -apple-system, sans-serif`), loaded with both axes: `wdth 62..125, wght 100..900`.

**Character:** One grotesque doing two jobs. At normal width and 400–650 weight it is the reading — spec values, body copy, card names. Compressed via `font-stretch` (88–96%) it becomes the instrument lettering: uppercase, wide-tracked, small. The width axis is why no second family exists in this system, and no second family may be added.

### Hierarchy
- **Display** (700, 3.5rem / 2.5rem below 560px, `font-stretch: 90%`, line-height 0.95, tracking -0.02em): the price amount in the detail readout. One per page, in amber.
- **Headline** (700, 2.25rem / 1.75rem below 560px, `font-stretch: 92%`): the listing name on the detail page.
- **Title** (600–700, 1.75rem): the result count on the catalog, gate titles.
- **Subtitle** (700, 1.375rem, `font-stretch: 92%`): the card price value, empty-state titles.
- **Lead** (600, 1.125rem, `font-stretch: 96%`): datasheet cell values, the wordmark, readout currency.
- **Body** (400, 0.9375rem, line-height 1.55): default page copy. Long-form prose caps at 68ch; the footer note at 46ch; empty-state notes at 44ch.
- **Small** (400–600, 0.8125rem): meta lines, help text, breadcrumbs, buttons, chips, pager.
- **Label** (600–650, 0.6875rem, `font-stretch: 88%`, tracking 0.12–0.22em, uppercase): the gauge label. Spec keys, rail legends, section titles, tags, field labels, result units.

### Named Rules
**The One Family Rule.** Archivo's width axis carries the entire condensed/gauge register. Never load a second family, a condensed static cut, or a monospace face for numerals — `font-variant-numeric: tabular-nums` is set globally on the body and already makes numbers align.

**The Gauge Label Rule.** Anything that names a value rather than being one is set in the label register: 11px, ~88% width, 600 weight, uppercase, tracked 0.12em or wider, in meta slate. Values are never uppercase; labels never sentence case.

## Layout

A 1440px shell (`--shell`) centered with 1.5rem gutters (1rem below 900px), on a 4px grid: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px.

**Catalog** is the defining composition: a 264px sticky filter rail on the left (`--rail`), a results bar with the count and sort on the right, a full-width tick rule beneath it, and an auto-filling card grid at `minmax(280px, 1fr)` with 24px gutters. The rail sticks 24px below the 60px masthead.

**Detail** is a two-column grid: content at `minmax(0, 1fr)` and a 380px sticky aside carrying the price readout and contact. The datasheet is a fixed 4-column grid with 1px gaps over a hairline background — the gap *is* the divider. Four columns is deliberate: the eight fields close in exactly two rows, and auto-fit left the last row half-empty.

**Auth** is a 420px centered gate — a side door, not a storefront.

**Responsive.** At ≤1000px the catalog collapses to one column and the rail becomes a drawer, closed by default so the grid starts in the first fold, with a circular amber count badge when filters are active. The detail collapses to one column and the aside moves to `order: -1`, putting price and contact above the gallery because they decide the next action. At ≤900px the masthead wraps and its secondary links become a horizontally scrolling strip while the amber CTA stays pinned outside that strip; form grids go single-column and form actions stack column-reverse. At ≤560px the type ramp shrinks at the root (display 2.5rem, h1 1.75rem), the card grid goes single column, and the datasheet drops to two columns.

**Named Rules**

**The Photo-Tolerance Rule.** The image archive is heterogeneous by nature — game screenshots, white-background cutouts, 1970s snapshots, irregular aspect ratios. Every photo therefore sits in a fixed covered frame (4:3 on cards and thumbs, 3:2 on the gallery stage) over a well-black backing, and any overlay on top of it is opaque or scrimmed. Never let intrinsic image proportions drive layout, and never assume a dark or a light photo.

## Elevation & Depth

There are no shadows anywhere in this system, and none may be added. Depth is tonal and linear: five plate values from the well (`#080A0D`) up through the floor, panel, and raised field, each separated by a 1px hairline. A card is "above" the page because it is one step lighter and outlined, not because it casts anything.

The only light effects in the build are emissive, not cast: a radial amber bloom inside the price readout (`radial-gradient(ellipse at top, amber-glow, transparent 62%)`), and scrims (72% / 82% well-black) under overlay chrome on photos. Hover elevation is a 2px lift plus a border brightening to graduation grey — motion and stroke, never shade.

### Named Rules
**The Hairline Rule.** Structure is drawn with 1px strokes and tonal steps. No box-shadow, no glow ring, no colored side stripe on an alert — an alert states its severity with a full 1px border plus a 12% wash, on all four sides.

## Shapes

Almost-square. An instrument panel is not rounded: 2px on small chrome (tags, chips, thumbnails, favorite buttons, badges), 3px on controls (buttons, inputs, nav links, alerts), 4px on containers (panels, cards, the rail, the gallery stage, the datasheet). The 999px pill exists as a token but is scoped to circular counters only — the mobile filter count badge is its sole use.

**The tick rule** is the system's signature geometry: a 10px-tall strip built from two repeating linear gradients — a fine graduation every 8px in graduation grey, and a taller, brighter mark every 40px — masked to fade out after 55% of its width so it reads as a scale running off the edge. Its lit variant (`--tick-rule--lit`) redraws both layers in amber and drops the mask; it appears once per detail page, under the price, where the reading rests.

Dashed 1px borders mark absence or provisional space: file drop zones, the empty catalog state, the safety note. Missing photos get a 135° 10/20px diagonal hatch in floor-over-well.

## Components

### Buttons
- **Shape:** near-square (3px), 0.75rem × 1.5rem padding, 13px 600-weight text, inline-flex with 8px gap for inline SVG.
- **Primary:** amber fill on well-black ink; hover brightens to filament amber. This is the commit action of a form and the seller's masthead entry.
- **Go:** signal-green fill on its dark counter-ink, used at `--lg` size (1rem × 2rem, 15px text) as the block-width WhatsApp button on the detail page. It is the product's terminal action and the only green button.
- **Ghost:** transparent with a hairline border and body-slate text; hover raises the border to disabled-slate and the text to readout white. The default for secondary and cancel actions.
- **Danger:** transparent with a stop-red border and red text; hover inverts to a red fill with white text.
- **Focus:** every interactive element takes a 2px amber outline at 2px offset, with a 2px radius, via `:focus-visible`.

### Chips
- **Style:** applied-filter tokens — 7% amber wash, dimmed-amber 1px border, amber-halo text, 2px corners, 13px.
- **State:** hover deepens the wash to 16%. The dismiss glyph is an amber 700-weight mark inside the chip; chips only ever represent an active filter.

### Tags
- **Style:** condition badges (`Novo` / `Seminovo` / `Usado`) in the label register with a 1px border and, critically, an **opaque well-black fill**. They sit on top of photographs; a translucent wash made the green `Novo` tag disappear against a light car body.
- **Colors:** green for novo, filament-amber on ember border for seminovo, secondary slate on hairline for usado.

### Cards / Containers
- **Corner Style:** 4px, overflow hidden so the image is clipped by the frame.
- **Background:** plate (`#14181E`) with a heavy-hairline border.
- **Shadow Strategy:** none — see Elevation & Depth. Hover raises the border to graduation grey and lifts the card 2px; the image inside scales to 1.03 over 0.4s.
- **Internal Padding:** 1rem body, with a 12px-padded top rule separating the price row from the data line.
- **Price row:** currency in 13px meta slate, value in 22px 700-weight amber at 92% width. It is the brightest element of the card by construction.

### Inputs / Fields
- **Style:** raised-plate fill (`#1A1F27`), hairline border, 3px radius, strong-body text, 12px padding. Labels are gauge labels in secondary slate; the required asterisk is amber.
- **Focus:** border shifts to amber and the fill *darkens* to plate — the field recedes as its edge lights up.
- **Filled filter:** in the rail, a field carrying a value takes an ember border, a 7% amber wash and readout-white text. This is the "indicator lit" state and it is driven by a `data-empty` attribute rendered server-side, not by JS.
- **Error:** the field border turns stop-red, with a 13px red message below; form-level errors get a bordered red-wash block.
- **File input:** dashed hairline border with a plate-grey `::file-selector-button`.

### Navigation
- **Style:** a 60px sticky masthead on well-black with a heavy hairline underneath. Links are 13px 500-weight secondary slate; hover fills with plate and raises text to white; the current page turns amber. The `Criar conta` link is a ghost variant with a hairline border.
- **Wordmark:** uppercase Archivo at 80% width, 700, with an amber interpunct separating the two halves and a 22%-tracked micro subtitle beside it (hidden below 560px). The brand is folded into the wordmark, never repeated as a kicker above page headings.
- **Mobile:** secondary links become a scrolling strip with hidden scrollbars; the amber CTA sits outside that strip in its own grid column so it can never scroll out of reach.

### Breadcrumbs, Pager, Alerts
- **Breadcrumbs:** 13px meta slate, links in secondary slate, hovering to amber.
- **Pager:** ghost-bordered links with inline SVG chevrons, a tabular-numeral "n / total" between them, above a hairline top rule; hover raises the border to ember and text to filament amber.
- **Alerts:** plate fill, 3px, 13px strong-body text, with the full border recolored by severity over a 12% wash. Info/debug use ember amber.

### Price Readout (signature)
The detail page's aside opens with the one truly lit object in the system: a plate panel bordered in ember amber, with a radial amber bloom bleeding from its top edge, a gauge-label key, a 56px amber amount at 90% width and 0.95 line-height beside an 18px currency mark, a **lit tick rule** at 70% opacity beneath the number, and a 13px meta note. Nothing else on any page may carry this much amber.

### Datasheet (signature)
Eight label/value cells in a 4-column grid whose 1px gaps expose a hairline background — the grid gap draws the ruling. Keys are gauge labels; values are 18px 600-weight readout white at 96% width; absent values drop to 15px 400-weight disabled slate. Its narrow sibling, the spec list, does the same job as label/value rows separated by hairlines, with values right-aligned.

### Motion
One authored moment: the dial warm-up on load. Tick rules sweep open left-to-right (`dial-sweep`, 0.7s, `cubic-bezier(0.16, 1, 0.3, 1)`) and price readings rise 4px into place (`dial-warmup`, 0.5s, 0.12s delay). Both use `backwards` fill so the resting state is the visible one — with animation disabled, nothing is missing. A global `prefers-reduced-motion: reduce` block collapses all durations to 0.01ms. Everything else is 0.15–0.18s state transitions on color, border and transform; those are support, never authorship.

**The One Moment Rule.** The dashboard warms up once, at load. Do not add a second authored animation, a scroll reveal, a looping pulse, or a parallax. New motion must either be a sub-0.2s state transition or nothing.

## Do's and Don'ts

### Do:
- **Do** start every surface on the floor (`#0F1216`) and build up through plate (`#14181E`) and raised plate (`#1A1F27`); a new surface earns its depth from a tonal step plus a 1px hairline.
- **Do** reserve amber for readings, active indicators and title rules; the audit test is "would a real instrument emit light here?"
- **Do** keep the two sanctioned amber exceptions exactly as they are — the masthead `Anunciar carro` CTA and the dirty-state apply button — and treat any third filled-amber surface as a defect.
- **Do** set every naming element in the gauge register (11px, ~88% width, uppercase, 0.12em+ tracking) and every value at normal width.
- **Do** use `font-stretch` on Archivo's `wdth` axis for any condensed need.
- **Do** put photographs in a fixed covered frame with an opaque or scrimmed overlay, so the heterogeneous archive sits evenly in a dense grid.
- **Do** divide sections with a tick rule, and use the lit variant only under a price.
- **Do** author icons as inline SVG in one stroke vocabulary (2–2.5px stroke, 11–15px box).
- **Do** keep numbers on tabular figures and Brazilian formatting (R$ 125.000,00).
- **Do** give every interactive element the 2px amber `:focus-visible` outline and keep the `prefers-reduced-motion` block intact.

### Don't:
- **Don't** add a box-shadow, a glow ring, or a colored side stripe on an alert; severity is a full 1px border plus a 12% wash.
- **Don't** use disabled slate (`#5E6878`) for body copy, placeholders or help text — it fails contrast; use `#9BA5B4` or lighter.
- **Don't** round anything past 4px; `--r-pill` is for circular counters only.
- **Don't** load a second typeface, a static condensed cut, or a monospace face for numerals.
- **Don't** put a brand kicker or eyebrow above a page heading; the brand lives in the wordmark and is folded into the heading itself.
- **Don't** use unicode arrows, emoji, or an icon font — chevrons and glyphs are authored inline SVG.
- **Don't** introduce a light surface, a white panel, or a light-mode variant; there is one world and it is night.
- **Don't** let green appear outside the `Novo` tag and the WhatsApp action, or red/orange outside error and warning states.
- **Don't** add a second authored animation; the dial warm-up is the system's one moment.
- **Don't** let any element out-brighten the price on its own screen.
