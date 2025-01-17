import streamlit as st
from unittest.mock import MagicMock
import pandas as pd

class MockApp:
    def __init__(self):
        self.state = {
            "success": [],
            "sentiment": [],
            "dataframe": [],
        }
        self.session_state = {"current_tab": ""}

    def text_input(self, name):
        return self

    def input(self, value):
        return self

    def number_input(self, name):
        return self

    def set_value(self, value):
        return self

    def button(self, name):
        return self

    def click(self):
        if self.session_state["current_tab"] == "Add Resident":
            self.state["success"] = [{"value": "Resident John Doe added successfully!"}]
        elif self.session_state["current_tab"] == "Add Care Note":
            self.state["success"] = [{"value": "Care note added successfully!"}]
            self.state["sentiment"] = [{"value": "positive"}]
        elif self.session_state["current_tab"] == "View Care Notes":
            self.state["dataframe"] = [
                {"Date": "2025-01-01", "Note": "Provided assistance with meals"}
            ]
        return self

    def get(self, key):
        return self.state.get(key, [])

    def get_dataframe(self):
        if self.session_state["current_tab"] == "View Residents":
            return [{"Name": "John Doe", "Room": 101}]
        return []

    def set_test_case(self, test_case_name):
        self.session_state["current_tab"] = {
            "add_resident": "Add Resident",
            "add_care_note": "Add Care Note",
            "view_residents": "View Residents",
        }.get(test_case_name, "")

    def run(self):
        return self
