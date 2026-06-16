import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-14: Logout success (*Đăng xuất thành công*)

    """
    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: chuyển sang tab "Mượn / Trả"
    logout_button = page.locator (
        'flt-semantics[role="button"]:has-text("Đăng xuất"), '
        'flt-semantics[role="button"]:has-text("Sign out")'
    ).first

    logout_button.click()

    # [P] Propagation: chờ quay lại màn hình đăng nhập
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_logout.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_login_button = (
        "Đăng nhập" in sem_text
        or "Sign In" in sem_text
    )

    has_email_input = "Email" in sem_text

    has_password_input = (
        "Mật khẩu" in sem_text
        or "Password" in sem_text
    )

    has_logout_button = (
        "Đăng xuất" in sem_text
        or "Sign out" in sem_text
    )


    assert has_login_button or has_email_input or has_password_input, \
        "Đăng xuất thất bại: không quay lại màn hình đăng nhập"

    assert not has_logout_button, \
        "Đăng xuất thất bại: vẫn còn thấy nút Đăng xuất/Logout"


def test_switch_language_to_english(page, test_config):
    """TC-15: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    """
    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: chuyển sang tab "Mượn / Trả"
    page.wait_for_timeout(2000)
    
    en_button = page.locator(
    'flt-semantics[role="button"]:has-text("EN")'
    ).first

    en_button.click(force=True)

    # [P] Propagation: chờ quay lại màn hình đăng nhập
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_switch_language_to_english.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_english_logout = "Sign out" in sem_text
    has_english_borrow = "Borrow" in sem_text
    has_english_library = "Library" in sem_text

    assert has_english_logout or has_english_borrow or has_english_library, \
        "Chuyển ngôn ngữ thất bại: không tìm thấy nội dung tiếng Anh trên giao diện"
