import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# ===============================
#        FILTROS DISPONÍVEIS
# ===============================
def apply_filter(img, filter_name):
    if filter_name == "Normal":
        return img

    elif filter_name == "Gray":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif filter_name == "Gaussian Blur":
        return cv2.GaussianBlur(img, (15, 15), 0)

    elif filter_name == "Median Blur":
        return cv2.medianBlur(img, 11)

    elif filter_name == "Sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)

    elif filter_name == "Canny":
        return cv2.Canny(img, 100, 200)

    elif filter_name == "Laplacian":
        return cv2.Laplacian(img, cv2.CV_64F)

    elif filter_name == "Red Channel":
        b, g, r = cv2.split(img)
        return r

    elif filter_name == "Green Channel":
        b, g, r = cv2.split(img)
        return g

    elif filter_name == "Blue Channel":
        b, g, r = cv2.split(img)
        return b

    return img


# ===============================
#           APLICAÇÃO
# ===============================
class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Editor de Imagem - Grau B")
        self.window.geometry("900x700")

        self.cap = cv2.VideoCapture(0)
        self.current_filter = "Normal"
        self.frame = None

        # Canvas para vídeo
        self.canvas = tk.Label(self.window)
        self.canvas.pack()

        # -------------------------------
        # Botões
        # -------------------------------
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Normal", width=12,
                  command=lambda: self.set_filter("Normal")).grid(row=0, column=0)

        tk.Button(btn_frame, text="Gray", width=12,
                  command=lambda: self.set_filter("Gray")).grid(row=0, column=1)

        tk.Button(btn_frame, text="Gaussian Blur", width=12,
                  command=lambda: self.set_filter("Gaussian Blur")).grid(row=0, column=2)

        tk.Button(btn_frame, text="Median Blur", width=12,
                  command=lambda: self.set_filter("Median Blur")).grid(row=0, column=3)

        tk.Button(btn_frame, text="Sharpen", width=12,
                  command=lambda: self.set_filter("Sharpen")).grid(row=1, column=0)

        tk.Button(btn_frame, text="Canny", width=12,
                  command=lambda: self.set_filter("Canny")).grid(row=1, column=1)

        tk.Button(btn_frame, text="Laplacian", width=12,
                  command=lambda: self.set_filter("Laplacian")).grid(row=1, column=2)

        tk.Button(btn_frame, text="Red", width=12,
                  command=lambda: self.set_filter("Red Channel")).grid(row=1, column=3)

        tk.Button(btn_frame, text="Green", width=12,
                  command=lambda: self.set_filter("Green Channel")).grid(row=2, column=0)

        tk.Button(btn_frame, text="Blue", width=12,
                  command=lambda: self.set_filter("Blue Channel")).grid(row=2, column=1)

        # Botão tirar foto
        tk.Button(self.window, text="📸 Tirar Foto", width=20, height=2,
                  command=self.take_photo).pack(pady=10)

        # Botão reset
        tk.Button(self.window, text="Resetar Filtros", width=20, height=2,
                  command=lambda: self.set_filter("Normal")).pack(pady=5)

        # Rodar loop do vídeo
        self.update_frame()
        self.window.mainloop()

    # Trocar filtro
    def set_filter(self, name):
        self.current_filter = name

    # Tirar foto e salvar
    def take_photo(self):
        if self.frame is not None:
            cv2.imwrite("foto_filtrada.png", self.frame)
            print("Foto salva como foto_filtrada.png!")

    # Atualizar vídeo
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Aplicar filtro
        processed = apply_filter(frame, self.current_filter)

        # Guardar última frame filtrada
        self.frame = processed.copy()

        # Converter para exibir no Tkinter
        if len(processed.shape) == 2:  # grayscale
            img = Image.fromarray(processed)
        else:
            img = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))

        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.configure(image=imgtk)

        # Atualizar a cada 10ms
        self.window.after(10, self.update_frame)


# ===============================
#        INICIAR PROGRAMA
# ===============================
App()
