# CipherX — Vintage Cryptographic UI/UX Design System (`design.md`)

## 1. Design Vision & Philosophy
The redesign transforms CipherX from a generic modern neon-dark theme into an authentic **Classical Cryptography Workbench**. The visual language is inspired by historical cipher machines, Alberti cipher disks, aged parchment manuscripts, typewriter dossiers, and intelligence decryption desks.

---

## 2. Color Palette & Token Definitions

| Token Name | Hex Code | Preview | Usage Description |
| :--- | :--- | :--- | :--- |
| `--color-parchment-bg` | `#F4EEDB` | Beige Parchment | Base page background and workstation floor |
| `--color-parchment-surface` | `#EFE8D6` | Aged Paper | Workstation panels, card containers, dialogs |
| `--color-parchment-input` | `#FDFBF7` | Clean Paper | Textarea input field, candidate cards |
| `--color-border-subtle` | `#D6CEBE` | Sepia Hairline | Container borders, card outlines, subtle dividers |
| `--color-border-dashed` | `#BDB3A1` | Typewriter Dash | Dashed section breaks, card headers |
| `--color-ink-primary` | `#2B2621` | Dark Charcoal Ink | Primary body text, labels, cipher wheel letters |
| `--color-ink-muted` | `#6E6659` | Faded Ink | Secondary descriptions, timestamps, help text |
| `--color-accent-crimson` | `#7E221D` | Oxblood / Red Wax | Circular stamp seal `(X)`, title accent, selected tags |
| `--color-status-matched` | `#5E7039` | Antique Olive Green | Identified cipher checklist item (`✓`), high-confidence mark |
| `--color-status-unmatched`| `#9C9281` | Muted Sepia Gray | Ruled-out cipher checklist item (`✕`) |
| `--color-status-active` | `#8C5A20` | Antique Amber | Live status indicator (`cipher identified - decrypting...`) |

---

## 3. Typography Hierarchy

- **Primary Heading**: Classic Serif (`Playfair Display`, `Georgia`, or Serif) with deep crimson accent.
- **Body & Workstation Mono**: Typewriter Monospace (`Courier Prime`, `Space Mono`, or `Courier New`).
- **Section Headers**: Tracked-out uppercase monospace with letter spacing (`tracking-widest`):
  ```
  CIPHERTEXT INPUT
  CLASSICAL CIPHER AUTO-DECRYPTION
  ```
- **Dividers**: Fine dashed horizontal borders (`border-b border-dashed border-[#BDB3A1]`).

---

## 4. UI Layout & Component Architecture

### 4.1 Header Bar
- **Stamp Seal**: A double-concentric circle enclosing `X` rendered in deep crimson (`#7E221D`).
- **Brand Title**: **CipherX** in an elegant serif typeface.
- **Subtitle**: `CLASSICAL CIPHER AUTO-DECRYPTION` in spaced monospace.
- **Mascot Accent**: A mini character dangling playfully from the top frame, preserving the signature visual element from the reference design.

### 4.2 Left Panel — "CIPHERTEXT INPUT"
1. **Panel Header**: Monospace uppercase title with horizontal dashed line.
2. **Cipher Mode**: `cipher_type: Auto Detect` (with dropdown option to pick a specific cipher or leave on automatic).
3. **Ciphertext Area**: Clean light-cream parchment textarea with vintage inner shadow and monospace letter spacing.
4. **Decryption Status**: Animated or highlighted text showing:
   `cipher identified - decrypting...`
5. **Cipher Candidate Checklist**:
   - `✓ Caesar Cipher` (Olive green text and checkmark)
   - `✕ Vigenère Cipher` (Muted sepia text and cross)
   - `✕ Atbash Cipher` (Muted sepia text and cross)
   - `✕ Affine Cipher` (Muted sepia text and cross)
   - `✓ Substitution Cipher` (Olive green text and checkmark)

### 4.3 Center Panel — "Interactive Cipher Wheel / Alberti Disk"
- **Outer Ring**: Stationary circular band containing letters A through Z evenly spaced around 360 degrees.
- **Inner Ring**: Rotatable concentric disc displaying the shifted cipher alphabet. For example, if shift is 3, D aligns with A.
- **Center Circle**: Crimson ring enclosing an antique checkmark `✓` or key indicator.
- **Tick Marks**: Delicate radial guide marks between rings for historical authenticity.
- **Dynamic Label**: `detected: Caesar Cipher` (or respective identified cipher algorithm).

### 4.4 Right Panel — "Decryption Results"
- **Plaintext Display**: Typewriter-style output card showing decrypted text with quick copy-to-clipboard button.
- **Candidate Cards**: Ranking list for multi-candidate decryptions with:
  - Cipher type & key parameters (e.g. `Shift: 3`, `Key: ENIGMA`, `a=5, b=8`)
  - Confidence / English score badge
  - Direct preview of decrypted candidate text

---

## 5. Responsive Behavior
- **Desktop (>= 1280px)**: 3-column workstation layout (Left: Input & Checklist, Center: Cipher Wheel, Right: Results).
- **Tablet (768px - 1279px)**: 2-column layout (Input & Wheel side-by-side, Results below).
- **Mobile (< 768px)**: Stacked single-column flow with responsive cipher disk scaling.
