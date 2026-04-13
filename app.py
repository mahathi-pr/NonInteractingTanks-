import os
import sys
import subprocess
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SimulationRunnerApp(QMainWindow):
    """
    PyQt6 GUI application to launch an OpenModelica-generated executable/batch file
    with start and stop time arguments.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.resize(760, 480)

        self.selected_app_path: Path | None = None

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select the application to launch (.exe or .bat)")
        self.path_input.setReadOnly(True)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_application)

        self.start_time_input = QSpinBox()
        self.start_time_input.setRange(0, 4)
        self.start_time_input.setValue(0)

        self.stop_time_input = QSpinBox()
        self.stop_time_input.setRange(1, 4)
        self.stop_time_input.setValue(4)

        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Execution output will appear here...")

        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._build_ui()

    def _build_ui(self) -> None:
        """Create and arrange all widgets."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.path_input)
        file_layout.addWidget(self.browse_button)

        form_layout = QFormLayout()
        form_layout.addRow("Application to launch:", file_layout)
        form_layout.addRow("Start time:", self.start_time_input)
        form_layout.addRow("Stop time:", self.stop_time_input)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(QLabel("Execution log:"))
        main_layout.addWidget(self.output_box)
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

    def browse_application(self) -> None:
        """Open file dialog for selecting executable or batch file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select OpenModelica Application",
            "",
            "Applications (*.exe *.bat);;All Files (*)",
        )

        if file_path:
            self.selected_app_path = Path(file_path)
            self.path_input.setText(file_path)
            self.output_box.append(f"Selected application: {file_path}")

    def validate_inputs(self) -> tuple[bool, str]:
        """Validate path and time constraints."""
        if self.selected_app_path is None:
            return False, "Please select an application to launch."

        if not self.selected_app_path.exists():
            return False, "The selected application does not exist."

        if self.selected_app_path.suffix.lower() not in {".exe", ".bat"}:
            return False, "Please select a valid .exe or .bat file."

        start_time = self.start_time_input.value()
        stop_time = self.stop_time_input.value()

        if not (0 <= start_time < stop_time < 5):
            return False, "Condition must satisfy: 0 <= start time < stop time < 5."

        return True, ""

    def build_environment(self, working_directory: Path) -> dict[str, str]:
        """
        Build environment variables for execution.

        The model folder is typically:
            NonInteractingTanks/
                bin/
                NonInteractingTanks.TwoConnectedTanks/

        So when the selected application is inside NonInteractingTanks.TwoConnectedTanks,
        the required OpenModelica DLLs are usually in the sibling ../bin folder.
        """
        env = os.environ.copy()

        candidate_bin_dir = working_directory.parent / "bin"
        if candidate_bin_dir.exists():
            env["PATH"] = str(candidate_bin_dir) + os.pathsep + env.get("PATH", "")

        return env

    def build_command(self) -> list[str]:
        """Build command-line arguments for the selected application."""
        assert self.selected_app_path is not None

        start_time = self.start_time_input.value()
        stop_time = self.stop_time_input.value()

        return [
            str(self.selected_app_path),
            f"-startTime={start_time}",
            f"-stopTime={stop_time}",
        ]

    def run_simulation(self) -> None:
        """Execute selected application with user-provided parameters."""
        is_valid, message = self.validate_inputs()
        if not is_valid:
            QMessageBox.warning(self, "Invalid Input", message)
            self.status_label.setText("Status: Invalid input")
            return

        assert self.selected_app_path is not None
        working_directory = self.selected_app_path.parent
        env = self.build_environment(working_directory)
        command = self.build_command()

        self.output_box.clear()
        self.output_box.append("Running command:")
        self.output_box.append(" ".join(command))
        self.output_box.append(f"Working directory: {working_directory}")
        self.output_box.append("-" * 70)

        try:
            self.status_label.setText("Status: Running simulation...")

            result = subprocess.run(
                command,
                cwd=str(working_directory),
                env=env,
                capture_output=True,
                text=True,
                shell=self.selected_app_path.suffix.lower() == ".bat",
                check=False,
            )

            if result.stdout.strip():
                self.output_box.append("STDOUT:")
                self.output_box.append(result.stdout)

            if result.stderr.strip():
                self.output_box.append("STDERR:")
                self.output_box.append(result.stderr)

            self.output_box.append("-" * 70)
            self.output_box.append(f"Return code: {result.returncode}")

            if result.returncode == 0:
                self.status_label.setText("Status: Simulation completed successfully")
                QMessageBox.information(
                    self,
                    "Success",
                    "Simulation completed successfully.",
                )
            else:
                self.status_label.setText("Status: Simulation failed")
                QMessageBox.critical(
                    self,
                    "Execution Failed",
                    f"Simulation failed with return code {result.returncode}. "
                    f"Please check the execution log.",
                )

        except Exception as exc:
            self.status_label.setText("Status: Unexpected error")
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred:\n{exc}",
            )


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)
    window = SimulationRunnerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()