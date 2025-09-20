from .main_page import MainPage
from .task_page import TaskPage
from .tracking_page import TrackingPage


# Просто создает страницу по индексу
class PageFactory:
    @staticmethod
    def createPage(page_index, page_name):
        if page_index == 0:
            return TrackingPage()
        elif page_index == 1:
            return TaskPage()
        elif page_index == 2:
            return MainPage()
        else:
            from .base_page import BasePage
            return BasePage(page_name)