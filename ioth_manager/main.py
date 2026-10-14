import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static
from textual.containers import Vertical

try:
    from native import get_bridge_version, init_stack
except ImportError:
    def get_bridge_version() -> str:
        return "0.1.0"

    def init_stack(name: str) -> bool:
        return True


class IoThManagerApp(App):
    """Interfaccia Textual con colori ANSI nativi dell'emulatore."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
    ]

    CSS = """
    Screen {
        background: ansi_default;
        color: ansi_default;
        padding: 1 2;
    }

    #stacks-box {
        border: solid ansi_green;
        border-title-color: ansi_green;
        background: ansi_default;
        height: 1fr;
    }

    #info-box {
        border: solid ansi_white;
        border-title-color: ansi_white;
        background: ansi_default;
        height: 6;
        margin-top: 1;
    }

    DataTable {
        background: ansi_default;
        color: ansi_default;
        height: 100%;
        padding: 0 2;
    }

    /* Rimuove lo sfondo predefinito delle righe e dell'header di DataTable */
    DataTable > .datatable--even-row,
    DataTable > .datatable--odd-row {
        background: ansi_default;
    }

    #table-stacks > .datatable--header {
        background: ansi_default;
        color: ansi_yellow;
        text-style: none;
    }

    #table-info > .datatable--header {
        background: ansi_default;
        color: ansi_white;
        text-style: none;
    }

    /* Barra di selezione della riga attiva con il grigio ANSI del terminale */
    DataTable > .datatable--cursor,
    DataTable:focus > .datatable--cursor {
        background: ansi_bright_black;
        color: ansi_bright_white;
        text-style: none;
    }

    #footer-keys {
        width: 100%;
        text-align: center;
        background: ansi_default;
        color: ansi_blue;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """
        la funzione compose viene chiamata all'avvio dell'app.
        Le yield sono le varie parti dell'interfaccia, vengono create in un ciclo (la yield rende i componenti dei generatori/iteratori).
        """
        with Vertical(id="stacks-box") as box_stacks:
            box_stacks.border_title = "IoTh Stacks"
            yield DataTable(id="table-stacks", show_cursor=True, zebra_stripes=False)

        with Vertical(id="info-box") as box_info:
            box_info.border_title = "Bridge"
            yield DataTable(id="table-info", show_cursor=False, zebra_stripes=False)

        yield Static(
            "␣ or ↵ Start/Stop  |  n New Stack  |  d Delete  |  k,↑ Up  |  j,↓ Down  |  q Quit",
            id="footer-keys",
        )

    def on_mount(self) -> None:
        """
        finita la composizione dell'interfaccia, viene eseguito on_mount, che popola le tabelle e inserisce la versione C.
        """
        # Imposta il tema ANSI puro se disponibile nella versione di Textual installata
        if "textual-ansi" in self.available_themes:
            self.theme = "textual-ansi"

        # 1. Tabella superiore: Stack IoTh
        # query_one cerca il widget specifico tramite il suo ID (#table-stacks)
        t_stacks = self.query_one("#table-stacks", DataTable)
        t_stacks.cursor_type = "row"
        t_stacks.add_columns("Stack Name", "Interface", "VDE Socket", "Active")

        t_stacks.add_row("ioth_net0", "vde0", "/tmp/vde.ctl", "true")
        t_stacks.add_row("ioth_lab1", "tap0", "/tmp/lab.ctl", "true")
        t_stacks.add_row("ioth_test", "veth0", "/tmp/test.ctl", "false")

        # 2. Tabella inferiore: Info Bridge C
        versione_c = get_bridge_version()
        t_info = self.query_one("#table-info", DataTable)
        t_info.add_columns("Name", "Host", "Backend", "Version", "Status")
        t_info.add_row("ioth0", "arch-btw", "libioth", versione_c, "On")

    def action_cursor_down(self) -> None:
        self.query_one("#table-stacks", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#table-stacks", DataTable).action_cursor_up()


if __name__ == "__main__":
    # ansi_color=True obbliga Textual a usare i 16 colori e la trasparenza del terminale
    app = IoThManagerApp(ansi_color=True)
    app.run()