import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-07: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability: login trước để vào trang chính
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: nhập keyword tìm kiếm (Sửa từ List thành String để tránh lỗi CI)
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Flutter"
    )

    # [P] Propagation: chờ kết quả xuất hiện
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_search_book_by_name.png"))

    # [R✓] Revealability: kiểm tra có kết quả Flutter
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    
    assert page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0, \
    "Không tìm thấy sách có chứa từ khóa Flutter"


def test_search_book_no_result(page, test_config):
    """TC-08: Search book – no results (*Tìm kiếm sách — không có kết quả*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability: login trước để vào trang chính
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: nhập keyword tìm kiếm (Sửa từ List thành String để phòng tránh lỗi CI)
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345"
    )

    # [P] Propagation: chờ kết quả xuất hiện
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_search_book_no_result.png"))

    # [R✓] Revealability: kiểm tra có kết quả Flutter
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    
    # Sửa lại câu thông báo lỗi cho đúng logic với assert == 0
    assert page.locator('flt-semantics[aria-label*="Mã: BOOK"]').count() == 0, \
    "Lỗi: Hệ thống vẫn hiển thị sách dù từ khóa tìm kiếm không tồn tại!"


def test_filter_by_category(page, test_config):
    """TC-09: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability: login trước để vào trang chính
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: nhập keyword tìm kiếm
    category = "Công nghệ"
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", category)

    # [P] Propagation: chờ kết quả xuất hiện
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_filter_by_category.png"))

    # [R✓] Revealability: kiểm tra có kết quả Flutter
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    book_count = book_cards.count()

    assert book_count > 0, f"Không tìm thấy sách nào sau khi lọc theo thể loại: {category}"

    for i in range(book_count):
        aria_label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert category.lower() in aria_label.lower(), f"Sách thứ {i + 1} không thuộc thể loại {category}. Nội dung: {aria_label}"


def test_search_by_author(page, test_config):
    """TC-10: Search book by author name (*Tìm kiếm sách theo tên tác giả*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability: login trước để vào trang chính
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: nhập keyword tìm kiếm (Sửa từ List thành String để tránh lỗi CI)
    author = "Nguyễn Minh Đức"
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        author
    )

    # [P] Propagation: chờ kết quả xuất hiện
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_search_by_author.png"))

    # [R✓] Revealability: kiểm tra có kết quả Flutter
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0, \
    "Không tìm thấy sách có tên tác giả Nguyễn Minh Đức"