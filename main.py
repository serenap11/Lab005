import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo", hint_text="Es. Chitarra")
    input_marca = ft.TextField(label="Marca", hint_text="Es. Yamaha")
    input_anno = ft.TextField(label="Anno", hint_text="Es. 2023")

    #contatore per il valore in euro dello strumento
    txt_valore = ft.Text(value="100.0", size=18, weight=ft.FontWeight.BOLD)

    def decrementa_valore(e):
        try:
            valore_attuale = float(txt_valore.value)
            if valore_attuale >= 10.0:
                txt_valore.value = f"{valore_attuale - 10.0}"
                page.update()
        except ValueError:
            pass

    def incrementa_valore(e):
        try:
            valore_attuale = float(txt_valore.value)
            txt_valore.value = f"{valore_attuale + 10.0}"
            page.update()
        except ValueError:
            pass

    btn_meno = ft.IconButton(icon="remove", on_click=decrementa_valore)
    btn_piu = ft.IconButton(icon="add", on_click=incrementa_valore)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_nuovo_strumento(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno = input_anno.value.strip()
        valore_str = txt_valore.value.strip()

        #campi vuoti
        if not tipo or not marca or not anno:
            alert.show_alert("Tutti i campi devono essere compilati")
            return

        #campo numerico
        try:
            anno_acquisto = int(anno)
        except ValueError:
            alert.show_alert("L'anno di acquisto deve essere un valore numerico")
            return

        try:
            valore = float(valore_str)
        except ValueError:
            alert.show_alert("Il valore in euro non è valido")
            return

        deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore)

        #svuotamento dei TextField
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        txt_valore.value = "100.0"

        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20, weight=ft.FontWeight.BOLD),
        ft.Row(spacing=10,
               controls=[input_tipo, input_marca, input_anno, pulsante_aggiungi],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=10,
               controls=[ft.Text("Valore (€):"), btn_meno, txt_valore, btn_piu],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(main)
