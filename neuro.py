import numpy as np
from PIL import Image
import os
from random import randint

SIZE = (32,32)
class Hopfild: # класс нейронной сети

  def __init__(self, n, k): # инициализация
    self.N = n # количество нейронов
    self.K = k # максимальное количсетво эпох распознавания сигнала
    self.W = np.zeros((n, n)) # матрица взаимодействий (весов)

  def remember(self, M): # метод запоминания образов
    for X in M: # перебор массива образов
      for i in range(self.N):
        for j in range(self.N):
          if i==j:
            self.W[i][j] = 0 # диагональные элементы матрицы полагаются равными нулю
          else:
            self.W[i][j] += X[i]*X[j] # можно опустить деление на N
    
  def associations(self, signal): # распознавание образа
    X = signal.copy() # текущее состояние
    stop=0

    while(stop<self.K):
      pre_X = X.copy() # предыдущее состояние
      for i in range(self.N):
        a_i = 0
        for j in range(self.N):
          a_i += self.W[i][j]*pre_X[j]
        X[i] = self.signum(a_i)

      if (pre_X==X).all(): # выход из цикла, если значения стабилизировались
        return X
      stop+=1
    return X

  def signum(self, a): # функция активации
    return 1 if a>=0 else -1

def create_image(base): # Создает бинарный вектор образа
  a = np.array([])
  for i in list(base.getdata()):
    a = np.append(a, -1 if i > 160 else 1)
  return a

def parse_image(img, dic, n): # Выводит образ по бинарному вектору
  a = ''
  for i in range(len(img)):
    if i % n == 0:
      print(a)
      a = ''
    a += dic[img[i]]

def print_images(img1, img2, dic, n):
  a1=''
  a2=''
  for i in range(len(img1)):
    if i%n==0:
      print(a1, ' '*10, a2)
      a1=''
      a2=''
    a1 += dic[img1[i]]
    a2 += dic[img2[i]]
  print('>'*32)
  
import numpy as np
from PIL import Image

def draw_image_from_array(arr, width=500, height=500):
    """
    Рисует изображение заданного размера на основе входного массива или списка:
      -1 → белый (255)
       1 → чёрный (0)

    :param arr: list или numpy.ndarray длины width*height или формы (height, width)
    :param width: желаемая ширина (pixels)
    :param height: желаемая высота (pixels)
    :return: PIL.Image.Image — объект 8-битного изображения в градациях серого ('L')
    """
    # Приводим к numpy-массиву
    a = np.asarray(arr)

    # Проверяем количество элементов
    expected_size = width * height
    if a.size != expected_size:
        raise ValueError(f"Ожидается общее число элементов {expected_size}, получено {a.size}")

    # Преобразуем в форму (height, width)
    if a.ndim == 1:
        a = a.reshape((height, width))
    elif a.ndim == 2:
        if a.shape != (height, width):
            raise ValueError(f"Ожидается форма ({height}, {width}), получено {a.shape}")
    else:
        raise ValueError(f"Неподдерживаемое число осей: {a.ndim}")

    # Маппим: -1 → 255, всё остальное → 0
    img_arr = np.where(a == -1, 255, 0).astype(np.uint8)

    # Создаём и возвращаем PIL Image
    img = Image.fromarray(img_arr, mode='L')
    return img

def learn_and_test():
  images_path = os.listdir("static/base_photo")
  imgs = [create_image(Image.open(f"static/base_photo/{x}").convert('L').resize(SIZE)) for x in images_path]
  # [Image.open(f"static/base_photo/{x}").convert('L').resize(SIZE).show() for x in images_path]
  print("#Векторизация картинок")
  images = np.array(imgs)

  signals_path = os.listdir("static/learn_photo")
  singns = [create_image(Image.open(f"static/learn_photo/{x}").convert('L').resize(SIZE)) for x in signals_path]
  print("#Векторизация картинок")
  signals = np.array(singns)
  
  NEURONS_NUMBER = SIZE[0]*SIZE[1] # 100 # количество нейронов
  MAX_STEPS = 100 # максимальное кол-во итераций

  h = Hopfild(NEURONS_NUMBER, MAX_STEPS)
  print("#Запоминание образов")
  h.remember(images)
  
  data_response = {"image":[]}

  senior = 0
  
  for signal in signals:
    res = h.associations(signal)
    
    senior+=1
    
    draw_image_from_array(signal, SIZE[0], SIZE[1]).save(f"static/render/{senior}_signal.jpg")
    draw_image_from_array(res, SIZE[0], SIZE[1]).save(f"static/render/{senior}_res.jpg")
    
    string = ''.join(["1" if x == 1 else "0" for x in list(res)])
    stringNew = ""
    for i in range(0, SIZE[0]*SIZE[1], 1):
      stringNew += string[i] if i % 32 != 0 else string[i] + "<br>"
      
    stringNew = stringNew[1::]
    stringNew += "0"
          
    data_response["image"].append({
      "img_render":f"static/render/{senior}_res.jpg",
      "img_signal":f"static/render/{senior}_signal.jpg",
      "str":stringNew
    })
    
    return data_response
    
if __name__ == "__main__":
  print(learn_and_test())