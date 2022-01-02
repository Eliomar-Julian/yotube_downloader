from imports import *


class MainWindow(Tk):
    TITLE = "Download Manager YouTube"
    SUB_TITLE = "Download de áudio e vídeos direto do youtube"
    CREDITS = "Criado e distribuido por Eliomar N. Julian"
    FONT = ("Roboto", 14)
    GRAND_FONT = ("Roboto", 25)
    GRAND_FONT_BOLD = ("Roboto", 25, "bold")
    LITTLE_FONT = ("Roboto", 8, "bold")
    COLS_TREE = ("Resolução", "Tamanho", "Tipo")
    COLS_TREE_A = ("Itag","Resolução", "Tamanho", "Tipo")

    def __init__(self):
        super(MainWindow, self).__init__()
        self.attributes("-zoomed", True)
        self.title(self.TITLE)
        self._logo = Image.open("./download.jpeg")
        self._logo_resize = ImageTk.PhotoImage(self._logo.resize((300, 200)))
        self.widgets()
        self.place_widgets()

    def widgets(self):
        self._main_frame = ttk.Frame(self, bootstyle=DEFAULT)
        self._show_title = ttk.Label(self._main_frame, bootstyle=DEFAULT, text=self.TITLE, font=self.GRAND_FONT)
        self._show_sub_title = ttk.Label(self._main_frame, bootstyle=DEFAULT, text=self.SUB_TITLE, font=self.FONT)
        self._search_bar = ttk.Entry(self._main_frame, style=DANGER, font=self.FONT)
        self._bt_search = ttk.Button(
            self._search_bar, text="Buscar", bootstyle="DANGER-OUTLINE", cursor="hand2", command=self.dont_freeze)
        self._show_credits = ttk.Label(self._main_frame, bootstyle=DEFAULT, text=self.CREDITS, font=self.LITTLE_FONT)
        self._sub_frame = ttk.Frame(self._main_frame, bootstyle=DEFAULT)
        self._thumbnail = ttk.Label(self._sub_frame, width=300, bootstyle=DARK, image=self._logo_resize)
        self._notbook = ttk.Notebook(self._sub_frame, bootstyle=DANGER, width=600)
        self._video_tab = ttk.Frame(self._notbook, bootstyle=DEFAULT, width=300)
        self._audio_tab = ttk.Frame(self._notbook, bootstyle=DEFAULT, width=300)
        self._treeview_video = ttk.Treeview(self._video_tab, columns=self.COLS_TREE, show=HEADINGS)
        self._treeview_audio = ttk.Treeview(self._audio_tab, columns=self.COLS_TREE_A, show=HEADINGS)
        for x in self.COLS_TREE: self._treeview_video.heading(x, text=x)
        for x in self.COLS_TREE_A: self._treeview_audio.heading(x, text=x)
        self._treeview_audio.column("Itag", width=40)
        self._meter = Meter(self._sub_frame, bootstyle=DANGER, textright="MB")
        self._title_video = ttk.Label(self._main_frame, text="Sem titulo...", bootstyle=DARK, font=self.FONT)
        self._status = ttk.Label(self._sub_frame, text="Aguardando", bootstyle=DANGER)
        self._search_bar.focus()

    def place_widgets(self):
        self._show_title.pack()
        self._show_sub_title.pack()
        self._main_frame.pack(fill=X, side=TOP)
        self._search_bar.pack(side=TOP, expand=TRUE, fill=X, ipady=10)
        self._bt_search.pack(side=RIGHT, padx=10)
        self._show_credits.pack(pady=10)
        self._sub_frame.pack(fill=X, pady=20)
        self._thumbnail.pack(side=LEFT, padx=10)
        self._notbook.pack(side=LEFT, anchor=N, padx=20)
        self._video_tab.pack(fill=BOTH, expand=TRUE)
        self._audio_tab.pack(fill=BOTH, expand=TRUE)
        self._notbook.add(self._video_tab, text="Vídeos")
        self._notbook.add(self._audio_tab, text="Áudios")
        self._treeview_video.pack(expand=TRUE, side=TOP)
        self._treeview_audio.pack(expand=TRUE, side=TOP)
        self._meter.pack(side=LEFT, anchor=N)
        self._title_video.pack()
        self._status.pack(side=LEFT, padx=10)
        

    def get_select(self, s):
        item = s.widget.focus()
        _dict = s.widget.item(item)
        self.download_ = self._yt.streams.get_by_resolution(_dict["values"][0])
        self.save = filedialog.askdirectory()
        Thread(target=self.downloading, daemon=True).start()

    def get_select_audio(self, s):
        item = s.widget.focus()
        _dict = s.widget.item(item)
        self.download_ = self._yt.streams.get_by_itag(_dict["values"][0])
        self.save = filedialog.askdirectory()
        Thread(target=self.downloading, daemon=True).start()


    def downloading(self):
        self._length_file = self.download_.filesize//(1024**2)
        self.update_bar_()
        
        self.download_.download(output_path=self.save, skip_existing=False)
        self._meter.configure(amounttotal=self._length_file)
        self._status.configure(bootstyle=SUCCESS, text="Cocluido")
    
    def update_bar_(self):
        #sleep(0.1)
        pro = 0
        try:
            pro = path.getsize(self.save + "/" + self.download_.default_filename)
        except:
            ...
        self._meter.configure(amountused=pro//(1024**2))
        if self._length_file >= pro:
            self._status.configure(bootstyle=WARNING, text="Baixando")
        self.update()
        self.after(1, self.update_bar_)
            



    

    def dont_freeze(self):
        self.th = Thread(target=self.search, daemon=True)
        self.th.start()
        #self._after = self.after(1, self.search)

    def search(self):
        self._yt = YouTube(self._search_bar.get())
        request.urlretrieve(self._yt.thumbnail_url, "./thumb.jpg")
        self._logo = Image.open("./thumb.jpg")
        self._logo_resize = ImageTk.PhotoImage(self._logo.resize((300, 200)))
        self._thumbnail["image"] = self._logo_resize
        tmp_title = str()
        for x in self._yt.title:
            if x.isascii(): tmp_title += x 
        self._title_video["text"] = tmp_title
        _filter = self._yt.streams.filter(progressive=True)
        _filter_audio = self._yt.streams.filter(only_audio=True)
        print(_filter_audio)

        for x in _filter_audio:
            print(x)

            # filtro de mime_type
            _tmp_str_t = str(x).index("mime_type")
            _tmp_fin_t = str(x)[_tmp_str_t:]
            _tmp_bla_t = _tmp_fin_t.index(" ")
            _fim_t = (str(x)[_tmp_str_t + 11: (_tmp_bla_t + _tmp_str_t) - 1])
            print(_fim_t)
            #####################################################################

            # filtro bit_rate
            _tmp_str = str(x).index("abr")
            _tmp_fin = str(x)[_tmp_str:]
            _tmp_bla = _tmp_fin.index(" ")
            _fim = (str(x)[_tmp_str + 5: (_tmp_bla + _tmp_str) - 1])
            #############################################################

            # filtro itag
            _tmp_str_i = str(x).index("itag")
            _tmp_fin_i = str(x)[_tmp_str_i:]
            _tmp_bla_i = _tmp_fin_i.index(" ")
            _fim_i = (str(x)[_tmp_str_i + 6: (_tmp_bla_i + _tmp_str_i) - 1])
            #############################################################

            self._treeview_audio.insert("", END, text=_fim, values=(_fim_i, _fim, x.filesize, _fim_t))


        # filtrando opções de video
        for x in _filter:

            # filtro de mime_type
            _tmp_str_t = str(x).index("mime_type")
            _tmp_fin_t = str(x)[_tmp_str_t:]
            _tmp_bla_t = _tmp_fin_t.index(" ")
            _fim_t = (str(x)[_tmp_str_t + 11: (_tmp_bla_t + _tmp_str_t) - 1])
            print(_fim_t)
            #####################################################################

            # filtro resolução
            _tmp_str = str(x).index("res")
            _tmp_fin = str(x)[_tmp_str:]
            _tmp_bla = _tmp_fin.index(" ")
            _fim = (str(x)[_tmp_str + 5: (_tmp_bla + _tmp_str) - 1])
            #############################################################
            
            self._treeview_video.insert("", END, text=_fim, values=(_fim, x.filesize, _fim_t))
            #self._treeview_audio.insert("", END, text=_fim, values=(_fim, x.filesize, _fim_t))

        self._treeview_video.bind("<Double-Button-1>", self.get_select)
        self._treeview_audio.bind("<Double-Button-1>", self.get_select_audio)
        self._meter.config(amountused=0)


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()