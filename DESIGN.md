# DESIGN.md — StoryWeaver: Novel-to-Video Pipeline

## Brand Overview

**Product**: StoryWeaver — Convert novels into animated visual stories
**Tagline**: Turn pages into cinema
**Tone**: Cinematic, warm, creative, premium but approachable

---

## Design System

### Colors

**Primary Palette**
- Primary: `#6C3BD5` (Deep Violet) — main actions, active states, links
- Primary Hover: `#7E4FE0`
- Primary Light: `#8B5CF6` (used for backgrounds, badges)
- Primary Dark: `#5B21B6`

**Secondary Palette**
- Secondary: `#D946EF` (Fuchsia) — accents, highlights, character tags
- Secondary Hover: `#E05DF0`
- Secondary Light: `#F0ABFC`

**Neutral Palette**
- Background: `#0F0F13` (deep charcoal — dark mode default)
- Background Alt: `#1A1A22` (cards, sidebars, elevated surfaces)
- Background Elevated: `#25252D` (modals, dropdowns, tooltips)
- Border: `#2D2D3A`
- Border Light: `#3A3A48`
- Text Primary: `#F5F5F7`
- Text Secondary: `#A1A1B2`
- Text Muted: `#6B6B80`
- White: `#FFFFFF`

**Semantic**
- Success: `#22C55E`
- Warning: `#F59E0B`
- Error: `#EF4444`
- Info: `#3B82F6`

**Surface Gradients**
- Card gradient: `linear-gradient(135deg, #1A1A22 0%, #1F1F2A 100%)`
- Hero gradient: `linear-gradient(180deg, #0F0F13 0%, #1A1A22 100%)`

---

### Typography

**Font Family**
- Headings: `'Space Grotesk', sans-serif` — modern, geometric, cinematic
- Body: `'Inter', sans-serif` — clean, highly readable
- Monospace: `'JetBrains Mono', monospace` — for code, timestamps

**Type Scale**

| Level | Size | Weight | Line Height | Tracking |
|---|---|---|---|---|
| Display | 48px / 3rem | 700 | 1.1 | -0.02em |
| H1 | 32px / 2rem | 700 | 1.2 | -0.02em |
| H2 | 24px / 1.5rem | 600 | 1.3 | -0.01em |
| H3 | 20px / 1.25rem | 600 | 1.4 | normal |
| H4 | 16px / 1rem | 600 | 1.4 | normal |
| Body Large | 16px / 1rem | 400 | 1.6 | normal |
| Body | 14px / 0.875rem | 400 | 1.6 | normal |
| Body Small | 13px / 0.8125rem | 400 | 1.5 | normal |
| Caption | 12px / 0.75rem | 500 | 1.4 | +0.02em |
| Overline | 11px / 0.6875rem | 700 | 1.2 | +0.08em |

---

### Spacing System (4px base)

| Token | PX | REM |
|---|---|---|
| space-1 | 4px | 0.25rem |
| space-2 | 8px | 0.5rem |
| space-3 | 12px | 0.75rem |
| space-4 | 16px | 1rem |
| space-5 | 20px | 1.25rem |
| space-6 | 24px | 1.5rem |
| space-8 | 32px | 2rem |
| space-10 | 40px | 2.5rem |
| space-12 | 48px | 3rem |
| space-16 | 64px | 4rem |

---

### Border Radius

| Token | Value | Usage |
|---|---|---|
| radius-sm | 6px | buttons small, inputs |
| radius-md | 10px | cards, dialogs |
| radius-lg | 16px | modals, panels |
| radius-xl | 24px | full-screen overlays |
| radius-full | 50% | avatars, badges |

---

### Shadows & Elevation

| Level | Shadow |
|---|---|
| low | `0 2px 4px rgba(0,0,0,0.3)` |
| mid | `0 4px 16px rgba(0,0,0,0.4)` |
| high | `0 8px 32px rgba(0,0,0,0.5)` |
| modal | `0 16px 48px rgba(0,0,0,0.6)` |
| glow-primary | `0 0 20px rgba(108, 59, 213, 0.3)` |

---

### Glass & Blur Effects

- Glass card: `background: rgba(37, 37, 45, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.06);`
- Frost sidebar: `background: rgba(15, 15, 19, 0.95); backdrop-filter: blur(12px);`

---

## Layout & Navigation

### App Shell
- Full-height viewport layout
- **Left sidebar**: 260px wide, collapsible to 64px (icon-only mode)
- **Top bar**: 56px height, fixed
- **Main content**: fills remaining space with 40px padding
- **Right panel** (Scene Editor only): 380px wide, slide-in

### Sidebar Navigation
- Background: Background Alt (#1A1A22)
- Width: 260px (expanded) / 64px (collapsed)
- Border-right: 1px solid Border
- Items: 44px height each, active state uses Primary background at 15% opacity
- Icon: 20px, aligned left with 16px padding
- Label: Body, 14px, Text Secondary
- Active: Text Primary, Primary icon, subtle left border (3px Primary)
- Section headers: Overline style, uppercase, Text Muted, padding top 24px

### Top Bar
- Fixed, 56px height
- Background: glass effect (frosted)
- Border-bottom: 1px solid Border
- Left: breadcrumb navigation (novel name > chapter > scene)
- Right: project status indicator, voice preview quick-play, user avatar

---

## Screens & Pages

### 1. Projects Dashboard
- **Hero banner**: gradient background, subtle animated pattern, app tagline
- **Grid layout**: 3-column responsive grid (2-col on tablet, 1-col on mobile)
- **Project card**: 
  - Thumbnail area (16:9 ratio, subtle gradient placeholder with novel title overlay)
  - Title (H4), author, chapter count, last modified date
  - Status badge: Draft / In Progress / Complete (colored pill)
  - Progress bar: thin 2px, linear from left to right, color Primary
  - Hover: slight translateY(-2px), glow-primary shadow, border highlight
- **Empty state**: centered illustration + "Import your first novel" CTA
- **Import button**: Primary, 40px height, icon + "Import Novel" label

### 2. Novel Detail / Character Bank
- **Two-column layout**: (60/40 split)
- **Left column — Chapter List**:
  - Chapter cards: numbered, title, scene count, duration estimate
  - Drag handle on left for reordering
  - Progress indicator per chapter (X/Y scenes complete)
- **Right column — Character Bank**:
  - Title "Characters" with count badge
  - Character cards:
    - Avatar (48px circle, generated portrait or initials fallback)
    - Name (Body Large, bold)
    - Role/tag (Caption, Secondary color pill)
    - Short description (Body Small, Text Muted, 2-line clamp)
    - Edit icon (pencil) on hover
  - "Extract Characters" button: triggers AI scan
  - Add character manually button (ghost style)

### 3. Scene Editor (Main Workflow)
- **Three-panel layout**:
  - **Left Panel** — Scene list / timeline (300px):
    - Vertical scene list with thumbnails (small 16:9)
    - Current scene highlighted with Primary left border
    - Numbering, narration snippet (1-line truncation)
    - Add scene button at bottom
  - **Center Panel** — Visual preview (flexible):
    - Large image/clip preview area
    - Ken Burns preview state (subtle zoom animation indicator)
    - Play/pause scrub bar at bottom
    - "Generate Image" button
    - Regenerate / variation buttons (ghost style)
  - **Right Panel** — Scene details (380px):
    - **Narration section**: textarea with character limit, word count
    - **Voice section**: 
      - Voice dropdown with play sample button (small play icon, 24px)
      - Voice name + gender tag
      - Speed slider: 0.8x - 1.2x
    - **Character tags**: inline pills showing which characters appear
    - **Camera motion**: dropdown (Static / Slow Zoom / Slow Pan / Dolly)
    - **Status**: Draft / Image Generated / Audio Generated / Compiled

- **Top breadcrumb**: Novel > Chapter 3 > Scene 5
- **Scene navigation arrows**: Previous / Next at top corners

### 4. Video Preview & Export
- **Full-width player** (16:9 or vertical 9:16 container):
  - Native-style video player
  - Play/pause, timeline scrub, volume, fullscreen
  - Timestamp overlay
- **Timeline below**: horizontal strip of scene thumbnails with durations
  - Active scene highlighted
  - Drag to reorder
- **Export controls**:
  - Format: MP4 / MOV
  - Resolution: 1080p / 720p
  - Aspect ratio: 16:9 / 9:16
  - Quality slider
  - "Export Video" button (Primary, large)

---

## UI Components

### Buttons

| Variant | Height | Padding | Style |
|---|---|---|---|
| Primary | 40px/44px | 16px 24px | Background Primary, text White, radius-md |
| Secondary | 40px | 16px 24px | Border 1px Border Light, text Text Primary, bg transparent |
| Ghost | 40px | 12px 16px | No border, text Text Secondary, hover text Text Primary |
| Icon | 36px/36px | 8px | Square, ghost style, icon 18px |
| Pill | 28px | 8px 14px | radius-full, small text |

States: hover (brightness 1.1), active (scale 0.97), disabled (opacity 0.4, no pointer)

### Inputs & Textareas
- Height: 44px (inputs), min 100px (textarea)
- Background: Background Alt
- Border: 1px solid Border, radius-md
- Focus: 2px Primary border, subtle glow
- Placeholder: Text Muted
- Label: Body Small, Text Secondary, 8px margin-bottom
- Helper text: Caption, Text Muted, 4px margin-top
- Error: border Error, Error text helper

### Cards
- Background: Background Alt with subtle gradient
- Border: 1px solid Border
- Radius: radius-md
- Padding: 16px
- Hover: mid shadow, border Primary Light at 30% opacity

### Badges / Pills
- radius-full
- Padding: 4px 10px
- Font: Caption, 500 weight
- Variants:
  - Default: Background Elevated, Text Secondary
  - Primary: Primary Light bg at 20%, Primary text
  - Success: Success at 15%, Success text
  - Warning: Warning at 15%, Warning text
  - Character tag: Secondary Light at 15%, Secondary Light text

### Tabs
- No background, border-bottom 1px Border
- Tab item: 14px, padding 12px 16px, Text Muted
- Active: Text Primary, border-bottom 2px Primary
- Hover: Text Secondary

### Modals / Dialogs
- Overlay: rgba(0,0,0,0.7), backdrop-filter blur(4px)
- Dialog: radius-lg, Background Elevated, max-width 640px, max-height 85vh
- Header: H4, 16px padding, border-bottom Border
- Body: 16px padding, scrollable
- Footer: 16px padding, border-top Border, right-aligned actions

### Progress Bars
- Height: 4px (default) / 2px (thin)
- Background: Background Elevated, radius-full
- Fill: linear-gradient(90deg, Primary, Secondary)
- Animated when active

### Skeleton Loaders
- Background: animated gradient shimmer
  - Base: Background Elevated
  - Shimmer: rgba(255,255,255,0.04)
- radius-md for blocks, radius-full for circles

### Toast / Notifications
- Position: bottom-right, 24px offset
- Max width: 420px
- Glass background with left colored border (Success/Warning/Error)
- Icon + message + dismiss X
- Auto-dismiss after 4s (success), manual for errors

---

## Animation & Motion

### Page Transitions
- Fade + subtle slide-up (8px, 300ms ease-out)
- Route changes: content crossfade 250ms

### Micro-interactions
- Button hover: scale(1.02), 150ms
- Button click: scale(0.97), 100ms
- Card hover: translateY(-2px), shadow transition, 200ms
- Skeleton: shimmer sweep 1.5s infinite

### Loading States
- Full page: centered spinner (Primary, 32px, border 3px)
- Inline: skeleton blocks matching layout shape
- Action: button shows spinner replacing icon, label hidden

---

## Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|---|---|---|
| Desktop | >1024px | Full 3-panel (Scene Editor), 3-col dashboard |
| Tablet | 768-1024px | Sidebar collapses to icons, 2-col dashboard |
| Mobile | <768px | Bottom nav bar replaces sidebar, single column |

---

## Iconography

Use Lucide icon set, 20px default size, stroke-width 1.5:
- Dashboard: `LayoutDashboard`
- Projects: `BookOpen`
- Characters: `Users`
- Scenes: `Clapperboard`
- Settings: `Settings`
- Play: `Play`
- Pause: `Pause`
- Generate: `Sparkles`
- Voice: `Mic2`
- Image: `ImagePlus`
- Export: `Download`
- Check: `CheckCircle2`
- Chevron: `ChevronRight`

---

## File & Asset Naming

- Character reference images: `char_{slug}_{id}.png` (1:1, 512x512)
- Scene keyframes: `scene_{chapter}_{scene}.png` (16:9, 1920x1080)
- Audio clips: `voice_{voice_name}_{scene_id}.mp3`
- Exported video: `{novel_slug}_ch{chapter}.mp4`

---

## Stitch-Specific Instructions

**Page list to generate (5 screens minimum)**:
1. Projects Dashboard
2. Novel Detail with Character Bank
3. Scene Editor (3-panel layout)
4. Video Preview & Export
5. Voice Selection Modal

**Design mode**: Dark theme only (the app is fully dark-mode native)
**Layout style**: Full-bleed, edge-to-edge with generous whitespace
**Export format**: HTML/CSS output
