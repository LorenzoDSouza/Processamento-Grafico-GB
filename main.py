import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

filter_descriptions = {
    "Normal": "Sem filtro aplicado. Retorna a imagem original.",
    "Gray": "Converte a imagem para escala de cinza.",
    "Gaussian Blur": "Aplica um borrão gaussiano para suavizar a imagem. Parâmetros: kernel (15,15).",
    "Median Blur": "Aplica um borrão mediano para reduzir ruído. Parâmetro: kernel 11.",
    "Sharpen": "Realça bordas usando um kernel de sharpen.",
    "Canny": "Detecta bordas usando o algoritmo Canny. Parâmetros: 100, 200.",
    "Laplacian": "Aplica o filtro Laplaciano para realce de bordas.",
    "Red Channel": "Exibe apenas o canal vermelho como imagem em cinza.",
    "Green Channel": "Exibe apenas o canal verde como imagem em cinza.",
    "Blue Channel": "Exibe apenas o canal azul como imagem em cinza.",
    "Addition": "Adiciona uma segunda imagem à atual (operação matemática).",
    "Subtraction": "Subtrai uma segunda imagem da atual (ponderada).",
    "Blending": "Mistura duas imagens com alpha=0.5 (blending)."
}

def apply_filter(img, filter_name, channel='all', second_img=None):
    if img is None:
        return None

    if filter_name == "Normal":
        return img

    if filter_name == "Gray":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return apply_to_channel(gray, channel, img)

    if filter_name == "Gaussian Blur":
        blurred = cv2.GaussianBlur(img, (15, 15), 0)
        return apply_to_channel(blurred, channel, img)

    if filter_name == "Median Blur":
        blurred = cv2.medianBlur(img, 11)
        return apply_to_channel(blurred, channel, img)

    if filter_name == "Sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(img, -1, kernel)
        return apply_to_channel(sharpened, channel, img)

    if filter_name == "Canny":
        edges = cv2.Canny(img, 100, 200)
        return apply_to_channel(edges, channel, img)

    if filter_name == "Laplacian":
        lap = cv2.Laplacian(img, cv2.CV_64F)
        lap = cv2.convertScaleAbs(lap)
        return apply_to_channel(lap, channel, img)

    if filter_name == "Red Channel":
        b, g, r = cv2.split(img)
        return r

    if filter_name == "Green Channel":
        b, g, r = cv2.split(img)
        return g

    if filter_name == "Blue Channel":
        b, g, r = cv2.split(img)
        return b

    if filter_name == "Addition":
        if second_img is not None:
            second_img_resized = cv2.resize(second_img, (img.shape[1], img.shape[0]))
            return cv2.add(img, second_img_resized)
        return img

    if filter_name == "Subtraction":
        if second_img is not None:
            second_img_resized = cv2.resize(second_img, (img.shape[1], img.shape[0]))
            return cv2.subtract(img, second_img_resized)
        return img

    if filter_name == "Blending":
        if second_img is not None:
            second_img_resized = cv2.resize(second_img, (img.shape[1], img.shape[0]))
            return cv2.addWeighted(img, 0.5, second_img_resized, 0.5, 0)
        return img

    return img

def apply_to_channel(processed, channel, original):
    if original is None:
        return processed

    if channel == 'all':
        if len(processed.shape) == 2:
            return cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
        return processed
    else:
        b, g, r = cv2.split(original)
        if len(processed.shape) == 3:
            processed_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        else:
            processed_gray = processed

        if channel == 'r':
            r = processed_gray
        elif channel == 'g':
            g = processed_gray
        elif channel == 'b':
            b = processed_gray

        r = ensure_channel_shape(r, original.shape[:2])
        g = ensure_channel_shape(g, original.shape[:2])
        b = ensure_channel_shape(b, original.shape[:2])
        return cv2.merge([b, g, r])

def ensure_channel_shape(ch, shape):
    if ch is None:
        return np.zeros(shape, dtype=np.uint8)
    ch = np.array(ch)
    if ch.dtype != np.uint8:
        ch = cv2.convertScaleAbs(ch)
    if ch.shape != shape:
        ch = cv2.resize(ch, (shape[1], shape[0]))
    return ch


def overlay(background, foreground, x, y):
    if background is None or foreground is None:
        return background

    if len(foreground.shape) < 3 or foreground.shape[2] != 4:
        return background

    bg_h, bg_w = background.shape[:2]
    fg_h, fg_w = foreground.shape[:2]

    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + fg_w, bg_w)
    y2 = min(y + fg_h, bg_h)

    if x1 >= x2 or y1 >= y2:
        return background

    fg_x1 = x1 - x
    fg_y1 = y1 - y
    fg_x2 = fg_x1 + (x2 - x1)
    fg_y2 = fg_y1 + (y2 - y1)

    roi_bg = background[y1:y2, x1:x2]
    roi_fg = foreground[fg_y1:fg_y2, fg_x1:fg_x2]

    alpha = roi_fg[:, :, 3:] / 255.0
    fg_rgb = roi_fg[:, :, :3].astype(float)
    bg_rgb = roi_bg.astype(float)

    blended = (alpha * fg_rgb + (1 - alpha) * bg_rgb).astype(np.uint8)
    background[y1:y2, x1:x2] = blended
    return background

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Editor de Imagem - Grau B")
        self.window.geometry("960x780")

        self.mode = 'video'
        self.cap = cv2.VideoCapture(0)

        self.current_filter = "Normal"
        self.current_channel = 'all'
        self.current_sticker = None
        self.current_sticker_path = None
        self.display_sticker = None
        self.sticker_pos = None
        self.frame = None
        self.original_frame = None
        self.photo_base = None
        self.second_image = None

        self.recording = False
        self.video_writer = None

        self.stickers = ["sticker1.png", "sticker2.png", "sticker3.png", "sticker4.png", "sticker5.png"]
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        self.canvas_w = 800
        self.canvas_h = 600
        self.canvas = tk.Canvas(self.window, width=self.canvas_w, height=self.canvas_h, bg='black')
        self.canvas.pack(pady=8)
        self.canvas.bind("<Button-1>", self.on_click)

        top_toolbar = tk.Frame(self.window, padx=4, pady=4)
        top_toolbar.pack()
        tk.Button(top_toolbar, text="Capturar Foto", width=16, command=self.take_photo).pack(side=tk.LEFT, padx=6)
        tk.Button(top_toolbar, text="Modo Vídeo", width=12, command=self.switch_to_video).pack(side=tk.LEFT, padx=6)
        tk.Button(top_toolbar, text="Modo Foto", width=12, command=self.switch_to_photo).pack(side=tk.LEFT, padx=6)

        stickers_toolbar = tk.Frame(top_toolbar)
        stickers_toolbar.pack(side=tk.RIGHT, padx=6)
        tk.Label(stickers_toolbar, text="Stickers:").pack(side=tk.LEFT, padx=(0,6))
        for i, s in enumerate(self.stickers):
            tk.Button(stickers_toolbar, text=f"S{i+1}", width=4,
                      command=lambda path=s: self.set_sticker(path)).pack(side=tk.LEFT, padx=2)

        self.create_ui()

        bottom_toolbar = tk.Frame(self.window, padx=6, pady=6, relief=tk.GROOVE)
        bottom_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(bottom_toolbar, text="Modo Vídeo", width=12, command=self.switch_to_video).pack(side=tk.LEFT, padx=6, pady=4)
        tk.Button(bottom_toolbar, text="Modo Foto", width=12, command=self.switch_to_photo).pack(side=tk.LEFT, padx=6, pady=4)
        tk.Button(bottom_toolbar, text="Capturar Foto", width=14, command=self.take_photo).pack(side=tk.LEFT, padx=6, pady=4)
        tk.Button(bottom_toolbar, text="Iniciar Gravação", width=14, command=self.start_recording).pack(side=tk.LEFT, padx=6, pady=4)
        tk.Button(bottom_toolbar, text="Parar Gravação", width=14, command=self.stop_recording).pack(side=tk.LEFT, padx=6, pady=4)
        tk.Button(bottom_toolbar, text="Remover Tudo", width=14, fg='red', command=self.clear_all).pack(side=tk.RIGHT, padx=6, pady=4)

        self.desc_label = tk.Label(self.window, text="", wraplength=900, justify=tk.LEFT)
        self.desc_label.pack(pady=6)

        self.update_frame()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.mainloop()

    def create_ui(self):
        main_frame = tk.Frame(self.window)
        main_frame.pack(pady=8, fill=tk.X)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=6)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, padx=12, anchor='n')

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack()

        filters = ["Normal", "Gray", "Gaussian Blur", "Median Blur", "Sharpen",
                   "Canny", "Laplacian", "Red Channel", "Green Channel", "Blue Channel"]
        row, col = 0, 0
        for f in filters:
            tk.Button(btn_frame, text=f, width=14,
                      command=lambda name=f: self.set_filter(name)).grid(row=row, column=col, padx=3, pady=3)
            col += 1
            if col > 3:
                col = 0
                row += 1

        ops_frame = tk.LabelFrame(right_frame, text="Operações", padx=6, pady=6)
        ops_frame.pack(fill=tk.X, pady=4)
        left_ops = tk.Frame(ops_frame)
        left_ops.pack(side=tk.LEFT, anchor='n', padx=(2,12))
        tk.Button(left_ops, text="Carregar Segunda Imagem", width=22, command=self.load_second_image).pack(pady=3)
        tk.Button(left_ops, text="Addition", width=22, command=lambda: self.set_filter("Addition")).pack(pady=3)
        tk.Button(left_ops, text="Subtraction", width=22, command=lambda: self.set_filter("Subtraction")).pack(pady=3)
        tk.Button(left_ops, text="Blending", width=22, command=lambda: self.set_filter("Blending")).pack(pady=3)

        stickers_frame = tk.LabelFrame(right_frame, text="Stickers", padx=6, pady=6)
        stickers_frame.pack(fill=tk.X, pady=4)
        for i, s in enumerate(self.stickers):
            tk.Button(stickers_frame, text=f"Sticker {i+1}", width=10,
                      command=lambda path=s: self.set_sticker(path)).grid(row=i//2, column=i%2, padx=4, pady=4)

        channel_frame = tk.LabelFrame(right_frame, text="Canais", padx=6, pady=6)
        channel_frame.pack(fill=tk.X, pady=4)
        tk.Button(channel_frame, text="All", width=6, command=lambda: self.set_channel('all')).pack(side=tk.LEFT, padx=3)
        tk.Button(channel_frame, text="Red", width=6, command=lambda: self.set_channel('r')).pack(side=tk.LEFT, padx=3)
        tk.Button(channel_frame, text="Green", width=6, command=lambda: self.set_channel('g')).pack(side=tk.LEFT, padx=3)
        tk.Button(channel_frame, text="Blue", width=6, command=lambda: self.set_channel('b')).pack(side=tk.LEFT, padx=3)

        extras_frame = tk.LabelFrame(right_frame, text="Extras", padx=6, pady=6)
        extras_frame.pack(fill=tk.X, pady=4)

        tk.Button(extras_frame, text="Capturar Foto", width=20, height=2, command=self.take_photo).pack(side=tk.TOP, pady=4)

        modes_frame = tk.Frame(extras_frame)
        modes_frame.pack(pady=4)
        tk.Button(modes_frame, text="Modo Vídeo", width=10, command=self.switch_to_video).pack(side=tk.LEFT, padx=4)
        tk.Button(modes_frame, text="Modo Foto", width=10, command=self.switch_to_photo).pack(side=tk.LEFT, padx=4)

        tk.Button(extras_frame, text="Iniciar/Parar Gravação", width=20, height=2, command=self.toggle_recording).pack(side=tk.TOP, pady=6)

        tk.Button(extras_frame, text="Resetar", width=12, height=2, command=self.reset).pack(side=tk.TOP, pady=4)
        tk.Button(extras_frame, text="Aplicar Filtro Face (Extra)", width=20, command=self.apply_face_filter).pack(side=tk.TOP, pady=4)

    def set_filter(self, name):
        self.current_filter = name
        self.desc_label.config(text=filter_descriptions.get(name, "Descrição não disponível."))
        print(f"Filtro selecionado: {name}")
        self.apply_current_filter()

    def set_channel(self, ch):
        self.current_channel = ch
        print(f"Canal selecionado: {ch}")
        self.apply_current_filter()

    def set_sticker(self, path):
        try:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is None:
                raise ValueError("Não foi possível carregar o sticker.")
            
            if img.shape[2] == 3:
                b, g, r = cv2.split(img)
                alpha = np.ones(b.shape, dtype=b.dtype) * 255
                img = cv2.merge([b, g, r, alpha])

            self.current_sticker = img
            self.display_sticker = None
            self.sticker_pos = None
            self.current_sticker_path = path
            print(f"Sticker selecionado: {path}")

            if self.mode == 'photo' and self.original_frame is not None:
                bg_h, bg_w = self.original_frame.shape[:2]
                fg = self.current_sticker.copy()
                fg_h, fg_w = fg.shape[:2]
                max_w = max(1, int(bg_w * 0.15))  
                max_h = max(1, int(bg_h * 0.15))
                scale = min(1.0, max_w / (fg_w + 1e-6), max_h / (fg_h + 1e-6))
                new_w = max(1, int(fg_w * scale))
                new_h = max(1, int(fg_h * scale))
                fg = cv2.resize(fg, (new_w, new_h), interpolation=cv2.INTER_AREA)
                self.display_sticker = fg
                x = random.randint(0, max(0, bg_w - new_w))
                y = random.randint(0, max(0, bg_h - new_h))
                self.sticker_pos = (x, y)
                self.original_frame = overlay(self.original_frame.copy(), self.display_sticker, x, y)
                self.frame = self.original_frame.copy()

        except Exception as e:
            print("Erro ao carregar sticker:", e)
            self.current_sticker = None
            self.display_sticker = None
            self.sticker_pos = None
            self.current_sticker_path = None

    def apply_current_filter(self):
        if self.original_frame is None:
            return
        try:
            processed = apply_filter(self.original_frame.copy(), self.current_filter, self.current_channel, self.second_image)
            if processed is None:
                return
            if len(processed.shape) == 2:
                processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
            self.frame = processed.copy()
        except Exception as e:
            print("Erro ao aplicar filtro:", e)

    def load_second_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            self.second_image = cv2.imread(file)
            print("Segunda imagem carregada:", file)
            self.apply_current_filter()

    def switch_to_video(self):
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        self.mode = 'video'
        self.original_frame = None
        self.frame = None
        print("Modo vídeo ativado.")

    def switch_to_photo(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            self.mode = 'photo'
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
            img = cv2.imread(file)
            if img is not None:
                self.photo_base = img.copy()
                self.original_frame = self.photo_base.copy()
                self.frame = self.original_frame.copy()
                print("Imagem carregada para modo foto:", file)
            else:
                print("Não foi possível carregar a imagem.")

    def on_click(self, event):
        if self.current_sticker is None or self.frame is None:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_h, img_w = self.frame.shape[:2]

        if canvas_w == 0 or canvas_h == 0:
            return

        scale_x = img_w / canvas_w
        scale_y = img_h / canvas_h

        click_x = int(event.x * scale_x)
        click_y = int(event.y * scale_y)

        top_left_x = click_x - self.current_sticker.shape[1] // 2
        top_left_y = click_y - self.current_sticker.shape[0] // 2

        if self.mode == 'photo' and self.original_frame is not None:
            self.original_frame = overlay(self.original_frame, self.current_sticker, top_left_x, top_left_y)
            self.frame = self.original_frame.copy()
        else:
            self.frame = overlay(self.frame, self.current_sticker, top_left_x, top_left_y)

        self.current_sticker = None
        self.current_sticker_path = None

    def take_photo(self):
        if self.frame is not None:
            filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")],
                                                    initialfile="resultado.png")
            if filename:
                cv2.imwrite(filename, self.frame)
                print("Imagem salva em:", filename)
            else:
                cv2.imwrite("resultado.png", self.frame)
                print("Imagem salva como resultado.png")

    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        filename = filedialog.asksaveasfilename(defaultextension=".avi",
                                                filetypes=[("AVI files", "*.avi"), ("MP4 files", "*.mp4")],
                                                initialfile="gravacao.avi")
        if not filename:
            print("Gravação não iniciada (nenhum arquivo escolhido).")
            return
        self.recording = True
        self.record_filename = filename
        self.video_writer = None
        print("Gravação iniciada:", filename)

    def stop_recording(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        self.recording = False
        print("Gravação parada.")

    def reset(self):
        self.current_filter = "Normal"
        self.current_channel = 'all'
        self.second_image = None
        self.current_sticker = None
        self.current_sticker_path = None
        self.desc_label.config(text="")
        if self.mode == 'photo' and self.original_frame is not None:
            self.frame = self.original_frame.copy()
        print("Reset realizado.")

    def apply_face_filter(self):
        if self.frame is None:
            return
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi = self.frame[y:y+h, x:x+w]
            blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)
            self.frame[y:y+h, x:x+w] = blurred_roi

        if self.mode == 'photo' and self.original_frame is not None:
            gray_o = cv2.cvtColor(self.original_frame, cv2.COLOR_BGR2GRAY)
            faces_o = self.face_cascade.detectMultiScale(gray_o, 1.3, 5)
            for (x, y, w, h) in faces_o:
                roi = self.original_frame[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)
                self.original_frame[y:y+h, x:x+w] = blurred_roi
            self.frame = self.original_frame.copy()
        print("Filtro de face aplicado em faces detectadas.")

    def update_frame(self):
        if self.mode == 'video':
            if self.cap is None:
                self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    self.window.after(30, self.update_frame)
                    return
                self.original_frame = frame.copy()
                processed = apply_filter(frame, self.current_filter, self.current_channel, self.second_image)
                if processed is None:
                    processed = frame.copy()
                else:
                    if len(processed.shape) == 2:
                        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

                if self.current_sticker is not None:
                    bg_h, bg_w = processed.shape[:2]

                    if getattr(self, 'display_sticker', None) is None:
                        fg = self.current_sticker.copy()
                        fg_h, fg_w = fg.shape[:2]
                        max_w = max(1, int(bg_w * 0.15))
                        max_h = max(1, int(bg_h * 0.15))
                        scale = min(1.0, max_w / (fg_w + 1e-6), max_h / (fg_h + 1e-6))
                        new_w = max(1, int(fg_w * scale))
                        new_h = max(1, int(fg_h * scale))
                        fg = cv2.resize(fg, (new_w, new_h), interpolation=cv2.INTER_AREA)
                        self.display_sticker = fg
                        x = random.randint(0, max(0, bg_w - new_w))
                        y = random.randint(0, max(0, bg_h - new_h))
                        self.sticker_pos = (x, y)

                    fg = self.display_sticker.copy()
                    x, y = self.sticker_pos if self.sticker_pos is not None else (bg_w - fg.shape[1], 0)
                    processed = overlay(processed, fg, x, y)

                self.frame = processed.copy()

        elif self.mode == 'photo' and self.frame is None:
            pass

        if self.recording and self.frame is not None:
            if self.video_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                h, w = self.frame.shape[:2]
                fps = 20.0
                try:
                    self.video_writer = cv2.VideoWriter(self.record_filename, fourcc, fps, (w, h))
                except Exception as e:
                    print("Erro ao criar VideoWriter:", e)
                    self.recording = False
                    self.video_writer = None

            if self.video_writer is not None:
                try:
                    self.video_writer.write(self.frame)
                except Exception as e:
                    print("Erro ao escrever frame:", e)

        if self.frame is not None:
            img_h, img_w = self.frame.shape[:2]
            scale = min(self.canvas_w / img_w, self.canvas_h / img_h)
            disp_w = int(img_w * scale)
            disp_h = int(img_h * scale)
            disp_frame = cv2.resize(self.frame, (disp_w, disp_h))
            disp_frame = cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(Image.fromarray(disp_frame))
            self.canvas.imgtk = imgtk
            self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=imgtk, anchor=tk.CENTER)

        self.window.after(30, self.update_frame)

    def on_close(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

    def clear_all(self):
        self.current_filter = "Normal"
        self.current_channel = 'all'
        self.second_image = None
        self.current_sticker = None
        self.current_sticker_path = None
        self.display_sticker = None
        self.sticker_pos = None
        if self.mode == 'photo' and self.photo_base is not None:
            self.original_frame = self.photo_base.copy()
            self.frame = self.original_frame.copy()
        else:
            self.frame = None
        if hasattr(self, 'desc_label') and self.desc_label is not None:
            self.desc_label.config(text="")
        print("Tudo removido (filtros e stickers).")

if __name__ == "__main__":
    App()

