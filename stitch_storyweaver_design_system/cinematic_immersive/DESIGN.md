---
name: Cinematic Immersive
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#cbc3d7'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#958ea0'
  outline-variant: '#494454'
  surface-tint: '#d0bcff'
  primary: '#d0bcff'
  on-primary: '#3b0091'
  primary-container: '#6c3bd5'
  on-primary-container: '#dfd1ff'
  inverse-primary: '#6d3cd6'
  secondary: '#fbabff'
  on-secondary: '#580065'
  secondary-container: '#ae05c6'
  on-secondary-container: '#ffd8fd'
  tertiary: '#4fdbc8'
  on-tertiary: '#003731'
  tertiary-container: '#006a5f'
  on-tertiary-container: '#64edd9'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5418bd'
  secondary-fixed: '#ffd6fd'
  secondary-fixed-dim: '#fbabff'
  on-secondary-fixed: '#36003e'
  on-secondary-fixed-variant: '#7c008e'
  tertiary-fixed: '#71f8e4'
  tertiary-fixed-dim: '#4fdbc8'
  on-tertiary-fixed: '#00201c'
  on-tertiary-fixed-variant: '#005048'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 64px
    fontWeight: '700'
    lineHeight: 72px
    letterSpacing: -0.02em
  display-md:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  sidebar_width: 260px
  topbar_height: 56px
  gutter: 24px
  margin_desktop: 40px
  stack_sm: 8px
  stack_md: 16px
  stack_lg: 32px
---

## Brand & Style
The design system focuses on a cinematic, high-fidelity experience tailored for desktop storytelling and creative workflows. It targets creators who require an immersive environment that minimizes distraction while maximizing expressive potential.

The aesthetic combines **Minimalism** with **Glassmorphism**. By using heavy background blurs and deep translucent layers, the UI feels like a sophisticated lens over a rich narrative world. The emotional response is one of focus, wonder, and professional creative agency. The dark theme is not merely a utility but a canvas that allows content to glow with a "neon-noir" sophistication.

## Colors
The palette is anchored in a cinematic dark theme. The primary Violet (#6C3BD5) acts as the main "active" signal, while the secondary Fuchsia (#D946EF) is reserved for moments of high creative energy or secondary highlights. 

- **Surface Tones:** The background uses a deep Navy-Slate (#0F172A). Higher elevation surfaces utilize semi-transparent variations of this base to allow background textures or blurs to bleed through.
- **Accents:** Tertiary Teal (#14B8A6) is used sparingly for success states or specialized creative tools.
- **Gradients:** Use a linear gradient (45deg) from Primary to Secondary for high-impact display moments and primary call-to-action buttons.

## Typography
The typographic hierarchy is designed for the high-density environment of a desktop application. **Space Grotesk** provides a technical, futuristic edge for all headings. For long-form reading and interface labels, **Inter** ensures maximum legibility. **JetBrains Mono** is utilized for metadata and technical labels to reinforce the "creator tool" feel.

On desktop, utilize `display-lg` for hero sections and chapter headings. Scale down to `headline-lg` for pane headers within the application shell. All uppercase labels should use `label-md` or `label-sm` with the specified letter spacing to maintain clarity on dark backgrounds.

## Layout & Spacing
The desktop application shell is structured around a **Persistent Left Sidebar** and a **Fixed Top Bar**.

- **App Shell:** The sidebar is fixed at 260px, providing a stable anchor for navigation. The top bar is 56px, housing contextual tools and breadcrumbs.
- **Main Content:** The workspace uses a fluid 12-column grid. On ultra-wide monitors, content is capped at 1440px width and centered to prevent eye strain.
- **Rhythm:** A base-8 unit system governs all spacing. Use 24px gutters for standard grids and 40px outer margins to provide "breathing room" for the cinematic aesthetic.
- **Density:** Maintain a generous "comfortable" density for the primary workspace, but allow the sidebar and utility panels to use "compact" spacing (8px-12px) for high-information density.

## Elevation & Depth
Depth is created through **Glassmorphism** and **Tonal Layering** rather than traditional drop shadows.

- **Level 0 (Base):** The deep #0F172A slate.
- **Level 1 (Sidebar/Top Bar):** A semi-transparent overlay (rgba(255, 255, 255, 0.03)) with a 20px backdrop blur and a subtle 1px inner border (rgba(255, 255, 255, 0.1)).
- **Level 2 (Cards/Modals):** A more opaque glass effect with a soft Primary-tinted ambient glow (e.g., a shadow with 40px blur, 0% spread, and 10% Primary color opacity).
- **Interactions:** Hover states should increase the backdrop blur intensity or brighten the inner border to simulate the element "lifting" toward the user.

## Shapes
The shape language balances the geometry of Space Grotesk with accessible softness. 

- **Containers:** Standard cards and panes use an 8px (0.5rem) radius.
- **Interactive Elements:** Buttons and input fields use a 16px (1rem) radius to feel more tactile and "human" against the rigid grid.
- **Selection States:** Use a "pill" shape (Full Radius) for active navigation indicators in the sidebar and for status chips.

## Components
- **Buttons:** Primary buttons use a linear gradient background (Violet to Fuchsia). Secondary buttons are "Ghost" style with a 1px Violet border. Use `label-md` for button text in all-caps.
- **Input Fields:** Dark, recessed backgrounds with a 1px border that glows Primary when focused. 
- **The Sidebar:** Navigation items should have a hover state that uses a subtle Primary-tinted glass effect. The active state includes a 4px vertical "light bar" on the left edge.
- **Cards:** Use Level 2 elevation. Ensure a 24px internal padding for content-heavy cards to maintain the cinematic "uncluttered" feel.
- **Chips:** Small, pill-shaped elements using `label-sm`. Success chips use the Tertiary Teal; warning chips use an Amber-tinted glass.
- **Scrollbars:** Custom slim, rounded scrollbars with a dark Primary-tinted track and a semi-transparent Violet thumb.