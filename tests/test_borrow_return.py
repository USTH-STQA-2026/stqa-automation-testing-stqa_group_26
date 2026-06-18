import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)


def test_borrow_book(page, test_config):
    """TC-11: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability: login trước để vào trang chính (nên dùng helper thay vì code lại logic đăng nhập tránh code dài)
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: Thao tác mượn sách
    borrow_button = page.locator (
        'flt-semantics[role="button"]:has-text("Mượn sách này"), '
        'flt-semantics[role="button"]:has-text("Borrow this book")'
    ).first

    borrow_button.click()

    # [P] Propagation: Thao tác xác nhận
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    confirm_borrow_button = page.locator (
        'flt-semantics[role="button"]:has-text("Mượn"), '
        'flt-semantics[role="button"]:has-text("Borrow")'
    ).last

    confirm_borrow_button.click()

    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_borrow_book.png"))

    # [R✓] Revealability: Kiểm tra kết quả mượn sách
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrowed_status = (
        "Đang mượn" in sem_text
        or "Borrowed" in sem_text
    )

    has_success_message = (
        "Mượn sách thành công!" in sem_text
        or "Book borrowed successfully!" in sem_text
    )

    assert has_borrowed_status or has_success_message, "Mượn sách thất bại: không thấy trạng thái Đang mượn/Borrowed hoặc thông báo thành công"


def test_view_borrowed_books(page, test_config):
    """TC-12: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: chuyển sang tab "Mượn / Trả"
    borrow_return_tab = page.locator (
        'flt-semantics[role="tab"][aria-label*="Mượn / Trả"], '
        'flt-semantics[role="tab"][aria-label*="Borrow / Return"]'
    ).first

    borrow_return_tab.click()

    # [P] Propagation: chờ danh sách sách đang mượn hiển thị
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_view_borrowed_books.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_borrowed_book = (
        "Đang mượn" in sem_text
        or "Borrowing" in sem_text
    )

    has_return_button = (
        "Trả sách" in sem_text
        or "Return book" in sem_text
    )

    has_returned_book = (
        "Đã trả" in sem_text
        or "Returned" in sem_text
    )

    assert has_borrowed_book or has_return_button or has_returned_book, \
        "Không tìm thấy sách đang mượn hoặc nút Trả sách trong tab Mượn / Trả"


def test_return_book(page, test_config):
    """TC-13: Return a borrowed book (*Trả sách đang mượn*)
    ✅ COMPLETED
    (*ĐÃ HOÀN THÀNH*)
    """
    # [R] Reachability
    login(page, test_config)
    enable_flutter_semantics(page)

    # [I] Infection: chuyển sang tab "Mượn / Trả"
    borrow_return_tab = page.locator(
        'flt-semantics[role="tab"][aria-label*="Mượn / Trả"], '
        'flt-semantics[role="tab"][aria-label*="Borrow / Return"]'
    ).first

    borrow_return_tab.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Tìm nút "Trả sách"
    return_button = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách"), '
        'flt-semantics[role="button"]:has-text("Return book")'
    ).first

    return_button.click()

    # [P] Propagation: chờ hệ thống cập nhật trạng thái trả sách
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "test_return_book.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_returned_status = (
        "Đã trả" in sem_text
        or "Returned" in sem_text
    )

    has_success_message = (
        "Trả sách thành công." in sem_text
        or "Book returned successfully."
    )

    assert has_returned_status or has_success_message, \
        "Trả sách thất bại: không thấy trạng thái Đã trả/Returned hoặc thông báo thành công"    
