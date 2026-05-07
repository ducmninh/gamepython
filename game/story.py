"""Story / chat dialog data and a simple chat-app UI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import pygame

from . import audio
from . import fonts
from . import settings as S
from . import sprites

HER = "her"
HIM = "him"


@dataclass
class Bubble:
    speaker: str   # HER or HIM
    text: str


INTRO: List[Bubble] = [
    Bubble(HER, "Anh ơi... Bông và 5 chú chó con bị bắt mất rồi 😭"),
Bubble(HER, "Em vừa quay vào bếp một lúc thôi mà ra đã không thấy chúng."),
Bubble(HIM, "Hả?? Em bình tĩnh, kể anh nghe."),
Bubble(HER, "Có mấy gã lạ mặt cứ rình quanh khu mình mấy hôm nay..."),
Bubble(HER, "Em thấy vết chân và một mẩu khăn đỏ ở cổng — chắc chắn là bọn trộm chó."),
Bubble(HIM, "Bọn này lại táo tợn vậy à. Em cứ ở nhà, anh đi tìm chúng."),
Bubble(HER, "Cẩn thận nha anh, chúng giữ từng con chó ở các mê cung khác nhau,"),
Bubble(HER, "và rải chìa khóa lung tung trong mê cung để không ai mở được."),
Bubble(HIM, "Anh sẽ giải cứu từng con một — từ chó con đến Bông. Hứa đó."),
]


LEVEL_INTROS = [
   f"Màn 1 — Tìm {S.PUPPY_NAMES[0]}! Khu vườn vắng — bọn trộm đang lởn vởn xa xa. Có một chòi nhỏ — vào đó là trộm không thấy anh đâu!",
f"Màn 2 — Tìm {S.PUPPY_NAMES[1]}! Hẻm tối — thêm bẫy gai và vài chòi trú. Anh nấp khi chúng đi ngang là an toàn.",
f"Màn 3 — Tìm {S.PUPPY_NAMES[2]}! Khu rừng hoang — mê cung phức tạp hơn. 2 tên trộm đang canh gác!",
f"Màn 4 — Tìm {S.PUPPY_NAMES[3]}! Hang động cổ đại — trong đây mù mịt lắm. 2 tên trộm đuổi anh!",
f"Màn 5 — Giải cứu {S.MOTHER_DOG_NAME}! Sào huyệt cuối cùng — 3 tên trộm hung hãn nhất. Cố lên anh ơi!",
]

OUTRO: List[Bubble] = [
  Bubble(HIM, f"Anh tìm được {S.MOTHER_DOG_NAME} và tất cả chó con rồi! 🐶"),
Bubble(HER, "Trời ơi... cảm ơn anh nhiều lắm 🥹"),
Bubble(HIM, f"{S.MOTHER_DOG_NAME} và 5 chú chó con đang vẫy đuôi mừng kia!"),
Bubble(HER, "Em mở cửa sẵn rồi. Về nhà với em đi anh."),
Bubble(HIM, "Cả đàn chó đã an toàn. Không ai có thể bắt chúng nữa!"),
]


# ------------------------------------------------------------------ #
class ChatScene:
    """Renders a chat-app style sequence of bubbles. The user advances by
    pressing Space/Enter. Typing animation reveals each bubble."""

    def __init__(self, bubbles: List[Bubble], title: str = "Tin nhan"):
        self.bubbles = bubbles
        self.title = title
        self.idx = 0
        self.char_idx = 0
        self.timer = 0
        self.font = fonts.get(18)
        self.title_font = fonts.get(22, bold=True)
        self.hint_font = fonts.get(16)

    def done(self) -> bool:
        return self.idx >= len(self.bubbles)

    def update(self) -> None:
        if self.done():
            return
        target = self.bubbles[self.idx].text
        if self.char_idx < len(target):
            self.timer += 1
            if self.timer >= 2:
                self.timer = 0
                self.char_idx += 1
                if target[self.char_idx-1] != " ":
                    audio.play_type()

    def advance(self) -> None:
        """Called on key press. If still typing -> finish current; else next bubble."""
        if self.done():
            return
        target = self.bubbles[self.idx].text
        if self.char_idx < len(target):
            self.char_idx = len(target)
        else:
            self.idx += 1
            self.char_idx = 0
            self.timer = 0

    def _wrap(self, text: str, max_w: int) -> List[str]:
        words = text.split(" ")
        lines: List[str] = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self.font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def draw(self, surf: pygame.Surface) -> None:
        surf.fill(S.PHONE_BG)
        # phone-frame
        frame = pygame.Rect(120, 40, S.SCREEN_W - 240, S.SCREEN_H - 80)
        pygame.draw.rect(surf, (28, 32, 42), frame, border_radius=24)
        pygame.draw.rect(surf, (60, 70, 90), frame, 3, border_radius=24)
        # title bar
        bar = pygame.Rect(frame.x, frame.y, frame.w, 56)
        pygame.draw.rect(surf, (40, 48, 64), bar, border_top_left_radius=24, border_top_right_radius=24)
        title_surf = self.title_font.render(self.title, True, S.WHITE)
        surf.blit(title_surf, (bar.x + 24, bar.y + 14))

        # avatars in title bar
        if sprites.GIRL_PORTRAIT:
            small = pygame.transform.scale(sprites.GIRL_PORTRAIT, (40, 40))
            surf.blit(small, (bar.right - 100, bar.y + 8))
        if sprites.BOY_PORTRAIT:
            small2 = pygame.transform.scale(sprites.BOY_PORTRAIT, (40, 40))
            surf.blit(small2, (bar.right - 52, bar.y + 8))

        # bubbles
        clip = pygame.Rect(frame.x + 8, bar.bottom + 8, frame.w - 16, frame.h - 80 - bar.h)
        prev_clip = surf.get_clip()
        surf.set_clip(clip)
        max_bubble_w = clip.w - 140
        # compute layout from the bottom up using the bubbles up to current index
        items = self.bubbles[: self.idx + 1]
        if not items:
            surf.set_clip(prev_clip)
            return
        rendered: List[Tuple[Bubble, List[str], List[str], int]] = []
        for i, b in enumerate(items):
            full_lines = self._wrap(b.text, max_bubble_w)
            shown_text = b.text if i < self.idx else b.text[: self.char_idx]
            shown_lines = self._wrap(shown_text, max_bubble_w)
            h = max(32, 12 + len(full_lines) * 22)
            rendered.append((b, full_lines, shown_lines, h))
        gap = 12
        total_h = sum(h for _, _, _, h in rendered) + gap * (len(rendered) - 1)
        y = clip.bottom - 12 - total_h

        for b, full_lines, shown_lines, h in rendered:
            text_w = max((self.font.size(l)[0] for l in full_lines), default=20)
            bubble_w = min(max_bubble_w, text_w + 24)
            if b.speaker == HER:
                rect = pygame.Rect(clip.x + 80, y, bubble_w, h)
                color = S.BUBBLE_HER
                if sprites.GIRL_PORTRAIT:
                    av = pygame.transform.scale(sprites.GIRL_PORTRAIT, (48, 48))
                    surf.blit(av, (clip.x + 12, y))
                tail = [(rect.left, rect.top + 14), (rect.left - 10, rect.top + 22), (rect.left, rect.top + 30)]
            else:
                rect = pygame.Rect(clip.right - 80 - bubble_w, y, bubble_w, h)
                color = S.BUBBLE_HIM
                if sprites.BOY_PORTRAIT:
                    av = pygame.transform.scale(sprites.BOY_PORTRAIT, (48, 48))
                    surf.blit(av, (clip.right - 60, y))
                tail = [(rect.right, rect.top + 14), (rect.right + 10, rect.top + 22), (rect.right, rect.top + 30)]
            pygame.draw.rect(surf, color, rect, border_radius=14)
            pygame.draw.polygon(surf, color, tail)
            for j, line in enumerate(shown_lines):
                surf.blit(self.font.render(line, True, (255, 255, 255)), (rect.x + 12, rect.y + 8 + j * 22))
            y += h + gap

        surf.set_clip(prev_clip)

        # hint at bottom
        hint = self.hint_font.render(
            "Space/Enter de tiep tuc — Esc de bo qua",
            True,
            (180, 180, 200),
        )
        surf.blit(hint, (frame.centerx - hint.get_width() // 2, frame.bottom - 32))
