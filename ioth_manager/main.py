from native import get_bridge_version, init_stack
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Input, Log


class IoThMiniApp(App):
    """Mini TUI essenziale per testare IoTh."""

    BINDINGS = [("q", "quit", "Esci")]

    def compose(self) -> ComposeResult:
        """
        la funzione compose viene chiamata all'avvio dell'app.
        Le yield sono le varie parti dell'interfaccia, vengono create in un ciclo (la yield rende i componenti dei generatori/iteratori).
        """
        yield Header()
        yield Input(placeholder="Nome dello stack (es. my_stack)...", id="stack_input")
        yield Button("Crea Stack", id="btn_create", variant="primary")
        yield Log(id="log_box")
        yield Footer()

    def on_mount(self) -> None:
        """
        finita la composizione dell'interfaccia, viene eseguito on_mount, che scrive la versione C nel log.
        """
        versione_c = get_bridge_version()
        # query_one cerca il primo widget Log e scrive la versione C nel log.
        self.query_one(Log).write_line(f"Bridge C collegato - Versione: {versione_c}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Eseguito quando premi il pulsante 'Crea Stack'."""
        input_widget = self.query_one(Input)
        log_box = self.query_one(Log)
        nome = input_widget.value.strip()

        if not nome:
            log_box.write_line("[!] Inserisci un nome prima di cliccare.")
            return

        # Chiamata alla funzione C (ctypes)
        ok = init_stack(nome)

        if ok:
            log_box.write_line(f"[OK] Stack '{nome}' creato con successo tramite C!")
            input_widget.value = ""  # Pulisce l'input
        else:
            log_box.write_line(f"[ERRORE] Il backend C ha rifiutato '{nome}'.")


if __name__ == "__main__":
    app = IoThMiniApp()
    app.run()
