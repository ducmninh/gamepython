"""Title screen, HUD side-panel, and end screens."""
from __future__ import annotations

from typing import List, Optional

import pygame
import math

from . import fonts
from . import settings as S
from . import sprites
from . import audio


class TitleScreen:
    def __init__(self):
        self.title_font = fonts.get(48, bold=True)
        self.font = fonts.get(22)
        self.small = fonts.get(18)
        self.micro = fonts.get(14)
        self.t = 0
        self.tabs = ["TRANG CHU", "HO SO", "LICH SU", "HUONG DAN", "CHUC NANG"]
        self.tab_idx = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.tab_idx = (self.tab_idx - 1) % len(self.tabs)
                audio.play_type()
            elif event.key == pygame.K_RIGHT:
                self.tab_idx = (self.tab_idx + 1) % len(self.tabs)
                audio.play_type()
            elif event.key == pygame.K_SPACE:
                return True # Start game
        return False

    def update(self):
        self.t += 1

    def draw(self, surf: pygame.Surface):
        surf.fill((10, 10, 25)) # Deep space black
        # Draw static stars
        rng = math.sin(self.t * 0.01) # Use time for subtle flicker if needed
        import random
        random.seed(42) # Consistent stars
        for _ in range(100):
            sx = random.randint(0, S.SCREEN_W)
            sy = random.randint(0, S.SCREEN_H)
            size = random.randint(1, 2)
            pygame.draw.circle(surf, (200, 200, 255), (sx, sy), size)

        # --- Draw Navigation Tabs ---
        tab_w = S.SCREEN_W // len(self.tabs)
        for i, name in enumerate(self.tabs):
            selected = i == self.tab_idx
            color = (0, 220, 255) if selected else (120, 100, 180)
            bg_color = (40, 20, 80) if selected else (20, 15, 40)
            pygame.draw.rect(surf, bg_color, (i * tab_w, 0, tab_w, 50))
            if selected:
                pygame.draw.rect(surf, (150, 100, 255), (i * tab_w, 0, tab_w, 50), 2)
                # Draw small cosmic fist icon for selection
                if hasattr(sprites, "FIST_LOGO") and sprites.FIST_LOGO:
                    f_small = pygame.transform.scale(sprites.FIST_LOGO, (24, 24))
                    # Tint fist blue-ish
                    surf.blit(f_small, (i * tab_w + 10, 13))
            
            txt = self.micro.render(name, True, color)
            surf.blit(txt, (i * tab_w + tab_w // 2 - txt.get_width() // 2, 15))

        # --- Central Background Logo (Fist) ---
        if hasattr(sprites, "FIST_LOGO") and sprites.FIST_LOGO:
            f_bg = pygame.transform.scale(sprites.FIST_LOGO, (400, 400))
            f_bg.set_alpha(40) # Faint background
            surf.blit(f_bg, (S.SCREEN_W // 2 - 200, S.SCREEN_H // 2 - 200))

        # --- Content Area ---
        if self.tab_idx == 0: # TRANG CHU
            title = self.title_font.render("GIẢI CỨU ĐÀN CHÓ", True, (0, 255, 255))
            surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 80))
            sub = self.font.render("Giải cứu 5 chó con và mẹ Bông từ bọn trộm!", True, (200, 180, 255))
            surf.blit(sub, (S.SCREEN_W // 2 - sub.get_width() // 2, 145))
            intro_story = self.small.render("Bạn vào vai người hùng xông pha vào sào huyệt bọn trộm để giải cứu gia đình Bông!", True, (160, 255, 160))
            surf.blit(intro_story, (S.SCREEN_W // 2 - intro_story.get_width() // 2, 180))

            if hasattr(sprites, "TITLE_DOG_IMAGE") and sprites.TITLE_DOG_IMAGE:
                big = pygame.transform.scale(sprites.TITLE_DOG_IMAGE, (300, 200))
                surf.blit(big, (S.SCREEN_W // 2 - 150, 210))
            
            if sprites.PUPPY_SPRITE:
                for i in range(5):
                    puppy = pygame.transform.scale(sprites.PUPPY_SPRITE, (48, 48))
                    x = S.SCREEN_W // 2 - 120 + i * 55
                    bounce = abs(math.sin(self.t * 0.08 + i * 0.5)) * 8
                    surf.blit(puppy, (x, 430 - bounce))

        elif self.tab_idx == 1: # HO SO
            title = self.font.render("HỒ SƠ NGƯỜI ANH HÙNG", True, (150, 200, 255))
            surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 100))
            
            # Character display
            chars = [
                {"name": "Anh Trai", "port": sprites.BOY_PORTRAIT, "desc": "Nhanh nhẹn, quyết đoán.", "x": S.SCREEN_W // 2 - 350},
                {"name": "Em Gái", "port": sprites.GIRL_PORTRAIT, "desc": "Khéo léo, can đảm.", "x": S.SCREEN_W // 2 + 200}
            ]
            for char in chars:
                if char["port"]:
                    p = pygame.transform.scale(char["port"], (128, 128))
                    surf.blit(p, (char["x"], 200))
                    n = self.font.render(char["name"], True, (255, 255, 255))
                    surf.blit(n, (char["x"] + 64 - n.get_width() // 2, 340))
                    d = self.small.render(char["desc"], True, (180, 180, 200))
                    surf.blit(d, (char["x"] + 64 - d.get_width() // 2, 380))

        elif self.tab_idx == 2: # LICH SU
            title = self.font.render("LỊCH SỬ GIẢI CỨU", True, (255, 230, 100))
            surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 100))
            msg = self.font.render("Chưa có dữ liệu lịch sử. Hãy bắt đầu hành trình!", True, (150, 150, 150))
            surf.blit(msg, (S.SCREEN_W // 2 - msg.get_width() // 2, 300))

        elif self.tab_idx == 3: # HUONG DAN
            title = self.font.render("HƯỚNG DẪN ĐIỀU KHIỂN", True, (255, 230, 100))
            surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 100))
            lines = [
                "Mũi tên hoặc WASD để di chuyển",
                "Nhặt đủ chìa khóa vàng trong mê cung để mở lồng",
                f"Giải cứu chó con ở mỗi màn — màn cuối giải cứu {S.MOTHER_DOG_NAME}!",
                "Tránh trộm — chúng dùng BFS đi tuần và A* đuổi anh!",
                "Nhặt đồng xu để mua đồ trong Shop sau mỗi màn!",
                "Nhan F để bật Toàn màn hình",
                "Phím T để dùng Dịch Chuyển (nếu có)",
                "Phím ENTER để bắn súng (nếu có)",
                "Phím Q để Ngưng đọng thời gian (nếu có)"
            ]
            for i, line in enumerate(lines):
                t = self.small.render(f"• {line}", True, (210, 210, 220))
                surf.blit(t, (150, 180 + i * 35))

        elif self.tab_idx == 4: # CHUC NANG
            title = self.font.render("CÁC CHỨC NĂNG CHÍNH", True, (255, 230, 100))
            surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 100))
            features = [
                ("Hệ thống Shop", "Mua vật phẩm nâng cấp sau mỗi màn chơi."),
                ("Radar thông minh", "Chỉ đường ngắn nhất đến mục tiêu (Bông/Nhà)."),
                ("Vật phẩm đặc biệt", "Giày tốc độ, Khiên phát quang, Súng lục..."),
                ("Đa dạng mức độ", "Nhiều màn chơi với độ khó tăng dần và kẻ trộm thông minh.")
            ]
            for i, (f_name, f_desc) in enumerate(features):
                n = self.font.render(f_name, True, (200, 255, 200))
                d = self.small.render(f_desc, True, (180, 180, 200))
                surf.blit(n, (150, 180 + i * 70))
                surf.blit(d, (170, 180 + i * 70 + 30))

        # --- Footer ---
        hint = self.micro.render("Dùng Mũi tên TRÁI/PHẢI để chuyển mục — SPACE để Bắt đầu", True, (200, 200, 220))
        surf.blit(hint, (S.SCREEN_W // 2 - hint.get_width() // 2, S.SCREEN_H - 60))

        if (self.t // 30) % 2 == 0:
            prompt = self.font.render("NHẤN SPACE ĐỂ CHƠI", True, (255, 240, 150))
            surf.blit(prompt, (S.SCREEN_W // 2 - prompt.get_width() // 2, S.SCREEN_H - 100))


class HUD:
    def __init__(self):
        self.font = fonts.get(20, bold=True)
        self.small = fonts.get(16)
        self.micro = fonts.get(12)

    def draw(self, surf: pygame.Surface, level_idx: int, level_name: str,
             keys_have: int, keys_total: int, hp: int, hp_max: int,
             dog_freed: bool, player_dfs_cooldown: int, player_dfs_timer: int,
             coins: int = 0, message: Optional[str] = None,
             dog_name: str = "", rescued_count: int = 0):

        # --- Top-Left: Level Info + Dog Name ---
        dog_label = f" | Giai cuu: {dog_name}" if dog_name else ""
        level_font = fonts.get(14, bold=True)
        level_txt = level_font.render(f"Man {level_idx + 1} | {level_name}{dog_label}", True, (250, 220, 100))
        self._draw_overlay_box(surf, (15, 15, level_txt.get_width() + 20, 30), level_txt)

        # --- Top-Right: Stats ---
        stats_w = max(hp_max * 28 + 10, 180)
        stats_surf = pygame.Surface((stats_w, 90), pygame.SRCALPHA)
        stats_surf.fill((20, 20, 30, 160))

        # hearts
        for i in range(hp_max):
            img = sprites.HEART_FULL if i < hp else sprites.HEART_EMPTY
            if img:
                stats_surf.blit(img, (10 + i * 28, 10))

        # keys
        if sprites.KEY_SPRITE:
            stats_surf.blit(sprites.KEY_SPRITE, (10, 40))
        kt = self.font.render(f"{keys_have}/{keys_total}", True, (255, 230, 130))
        stats_surf.blit(kt, (42, 44))

        # coins
        coin_txt = self.font.render(f"Xu: {coins}", True, (255, 230, 100))
        stats_surf.blit(coin_txt, (10, 68))

        surf.blit(stats_surf, (S.SCREEN_W - stats_w - 15, 15))

        # --- Rescued dogs counter ---
        rescued_txt = self.small.render(f"Da cuu: {rescued_count}/6 cho", True, (150, 255, 150))
        rescued_bg = pygame.Surface((rescued_txt.get_width() + 16, rescued_txt.get_height() + 8), pygame.SRCALPHA)
        rescued_bg.fill((20, 20, 30, 160))
        rescued_bg.blit(rescued_txt, (8, 4))
        surf.blit(rescued_bg, (S.SCREEN_W - stats_w - 15, 110))

        # --- Bottom-Left: DFS + Controls ---
        dfs_w = 240
        dfs_h = 80
        dfs_surf = pygame.Surface((dfs_w, dfs_h), pygame.SRCALPHA)
        dfs_surf.fill((20, 20, 30, 160))

        dfs_color = (200, 100, 255) if player_dfs_cooldown == 0 else (100, 100, 120)
        dfs_label = self.small.render("[G] DFS Radar: ", True, (220, 220, 240))
        dfs_status = "SAN SANG" if player_dfs_cooldown == 0 else f"Hoi chieu ({player_dfs_cooldown // 60}s)"
        dfs_val = self.small.render(dfs_status, True, dfs_color)
        dfs_surf.blit(dfs_label, (10, 10))
        dfs_surf.blit(dfs_val, (10, 30))

        hint = self.micro.render("WASD: Di chuyen | G: Radar | T: Dich chuyen | F: Fullscreen", True, (160, 160, 180))
        dfs_surf.blit(hint, (10, 55))

        surf.blit(dfs_surf, (15, S.SCREEN_H - dfs_h - 15))

        # --- Bottom-Right: Algorithm Legend ---
        leg_w = 180
        leg_h = 60
        leg_surf = pygame.Surface((leg_w, leg_h), pygame.SRCALPHA)
        leg_surf.fill((20, 20, 30, 160))

        legend = [
            ("Vang: BFS (Tuan tra)", S.GOLD),
            ("Do: A* (Duoi bat)", S.TRAP_RED),
            ("Tim: DFS (Radar)", (200, 100, 255)),
        ]
        for i, (txt, col) in enumerate(legend):
            t = self.micro.render(txt, True, col)
            leg_surf.blit(t, (10, 5 + i * 18))

        surf.blit(leg_surf, (S.SCREEN_W - leg_w - 15, S.SCREEN_H - leg_h - 15))

        if message:
            self._draw_message(surf, message)

    def _draw_overlay_box(self, surf, rect_coords, text_surf):
        x, y, w, h = rect_coords
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((20, 20, 30, 160))
        surf.blit(bg, (x, y))
        surf.blit(text_surf, (x + 10, y + (h - text_surf.get_height()) // 2))

    def _draw_message(self, surf, message):
        font = fonts.get(16, bold=True)
        text = font.render(message, True, (255, 255, 255))
        bg = pygame.Surface((text.get_width() + 20, text.get_height() + 10), pygame.SRCALPHA)
        bg.fill((20, 20, 30, 160))
        bg.blit(text, (10, 5))
        surf.blit(bg, (S.SCREEN_W // 2 - bg.get_width() // 2, S.SCREEN_H - 70))


class EndScreen:
    def __init__(self, won: bool):
        self.won = won
        self.title_font = fonts.get(54, bold=True)
        self.font = fonts.get(22)
        self.t = 0

    def update(self):
        self.t += 1

    def draw(self, surf: pygame.Surface):
        surf.fill((18, 22, 32) if self.won else (40, 18, 22))
        if self.won:
            title = self.title_font.render(f"DA CUU DUOC {S.MOTHER_DOG_NAME.upper()} VA CA DAN CHO!", True, (250, 220, 100))
            sub = self.font.render("Ca dan cho an toan tro ve. Cam on anh hung nho!", True, (220, 220, 240))
        else:
            title = self.title_font.render("Bi bat mat roi...", True, (250, 130, 140))
            sub = self.font.render("Nhan R de thu lai, Esc de thoat.", True, (220, 220, 240))
        surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 140))
        surf.blit(sub, (S.SCREEN_W // 2 - sub.get_width() // 2, 220))

        if self.won:
            # Draw the whole dog family
            if sprites.DOG_SPRITE:
                d = pygame.transform.scale(sprites.DOG_SPRITE, (120, 120))
                surf.blit(d, (S.SCREEN_W // 2 - 60, 280))
            if sprites.PUPPY_SPRITE:
                for i in range(5):
                    p = pygame.transform.scale(sprites.PUPPY_SPRITE, (48, 48))
                    x = S.SCREEN_W // 2 - 120 + i * 55
                    bounce = abs(math.sin(self.t * 0.1 + i * 0.7)) * 10
                    surf.blit(p, (x, 400 - bounce))

        prompt = self.font.render("Nhan SPACE de choi lai tu dau", True, (255, 240, 150))
        if (self.t // 30) % 2 == 0:
            surf.blit(prompt, (S.SCREEN_W // 2 - prompt.get_width() // 2, 500))


class CharSelect:
    def __init__(self):
        self.skins = ["Boy", "Girl", "Ninja"]
        self.idx = 0
        self.font = fonts.get(28, bold=True)
        self.small = fonts.get(18)
        self.t = 0

    def update(self):
        self.t += 1

    def draw(self, surf: pygame.Surface):
        surf.fill((10, 10, 25)) # Deep space black
        # Draw static stars
        import random
        random.seed(42)
        for _ in range(80):
            sx = random.randint(0, S.SCREEN_W)
            sy = random.randint(0, S.SCREEN_H)
            size = random.randint(1, 2)
            pygame.draw.circle(surf, (200, 200, 255), (sx, sy), size)

        title = self.font.render("CHỌN NHÂN VẬT", True, (0, 255, 255))
        surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 80))

        for i, skin in enumerate(self.skins):
            selected = i == self.idx
            color = (0, 255, 255) if selected else (120, 120, 180)
            txt = self.font.render(skin, True, color)
            x = S.SCREEN_W // 2 - 250 + i * 250
            y = 380

            preview = sprites.PLAYER_SKINS[skin]["A"]
            prev_scaled = pygame.transform.scale(preview, (140, 140))
            
            if selected:
                bounce = abs(math.sin(self.t * 0.1)) * 15
                # Glowing aura behind selected character
                glow_size = 160 + math.sin(self.t * 0.1) * 10
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (0, 150, 255, 60), (glow_size // 2, glow_size // 2), glow_size // 2)
                surf.blit(glow_surf, (x - glow_size // 2, y - 160 - bounce))
                
                surf.blit(prev_scaled, (x - 70, y - 170 - bounce))
                # Add selection box
                pygame.draw.rect(surf, (150, 100, 255), (x - 80, y - 180 - bounce, 160, 210), 3, border_radius=10)
            else:
                surf.blit(prev_scaled, (x - 70, y - 170))

            surf.blit(txt, (x - txt.get_width() // 2, y))

        hint = self.small.render("Dùng Mũi tên để chọn — SPACE để bắt đầu", True, (200, 180, 255))
        surf.blit(hint, (S.SCREEN_W // 2 - hint.get_width() // 2, S.SCREEN_H - 100))


class ShopScreen:
    def __init__(self, coins: int, level_idx: int):
        self.coins = coins
        self.level_idx = level_idx
        self.items = [
            {"id": "speed", "name": "Giay Than Toc", "cost": 100, "desc": "Tang 50% toc do chay"},
            {"id": "key", "name": "Chia Khoa Vang", "cost": 50, "desc": "Bat dau voi 1 chia khoa"},
            {"id": "teleport", "name": "Dich Chuyen", "cost": 150, "desc": "Phim T de ve nha tru an"},
            {"id": "gun", "name": "Sung Luc (2 vien)", "cost": 150, "desc": "Phim ENTER de ban trom"},
            {"id": "stop", "name": "Ngung Dong Thoi Gian", "cost": 250, "desc": "Phim Q: Dung trom 5 giay"},
            {"id": "shield", "name": "Khien Phat Quang", "cost": 200, "desc": "Chan 1 lan sat thuong tu lua"},
        ]
        self.idx = 0
        self.font = fonts.get(18, bold=True)
        self.small = fonts.get(14)
        self.bought = set()

    def update(self):
        pass

    def draw(self, surf: pygame.Surface):
        overlay = pygame.Surface((S.SCREEN_W, S.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surf.blit(overlay, (0, 0))

        shop_w = S.SCREEN_W - 300
        shop_h = S.SCREEN_H - 120
        pygame.draw.rect(surf, (40, 50, 80), (150, 60, shop_w, shop_h))
        pygame.draw.rect(surf, (255, 230, 100), (150, 60, shop_w, shop_h), 3)

        title = self.font.render("CUA HANG NANG CAP", True, (255, 230, 100))
        surf.blit(title, (S.SCREEN_W // 2 - title.get_width() // 2, 80))

        coins_txt = self.font.render(f"Xu cua ban: {self.coins}", True, (255, 215, 0))
        surf.blit(coins_txt, (S.SCREEN_W // 2 - coins_txt.get_width() // 2, 115))

        # Draw shop keeper
        if sprites.SHOP_KEEPER_SPRITE:
            keeper = pygame.transform.scale(sprites.SHOP_KEEPER_SPRITE, (80, 80))
            surf.blit(keeper, (170, 75))

        for i, item in enumerate(self.items):
            y = 150 + i * 65
            selected = i == self.idx
            bought = item["id"] in self.bought
            can_afford = self.coins >= item["cost"]

            bg_color = (60, 80, 120) if selected else (40, 50, 80)
            if bought:
                bg_color = (30, 60, 30)
            pygame.draw.rect(surf, bg_color, (180, y, shop_w - 60, 55))
            if selected:
                pygame.draw.rect(surf, (255, 230, 100), (180, y, shop_w - 60, 55), 2)

            name_color = (150, 150, 150) if bought else ((255, 255, 255) if can_afford else (200, 100, 100))
            name = self.font.render(item["name"], True, name_color)
            cost = self.small.render(f"{item['cost']} xu" if not bought else "DA MUA", True,
                                     (100, 200, 100) if bought else ((255, 215, 0) if can_afford else (200, 100, 100)))
            desc = self.small.render(item["desc"], True, (180, 180, 200))

            surf.blit(name, (200, y + 5))
            surf.blit(cost, (shop_w + 100 - cost.get_width(), y + 5))
            surf.blit(desc, (200, y + 28))

        hint = self.small.render("UP/DOWN: Chon | ENTER: Mua | SPACE: Tiep tuc man tiep theo", True, (200, 200, 220))
        surf.blit(hint, (S.SCREEN_W // 2 - hint.get_width() // 2, S.SCREEN_H - 130))

        next_lvl = self.level_idx + 2
        if next_lvl <= len(S.LEVELS):
            next_cfg = S.LEVELS[self.level_idx + 1]
            next_txt = self.small.render(f"Man tiep theo: {next_cfg['name']} ({next_cfg['thieves']} trom)", True, (180, 220, 255))
            surf.blit(next_txt, (S.SCREEN_W // 2 - next_txt.get_width() // 2, S.SCREEN_H - 100))
