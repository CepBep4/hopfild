import numpy as np
from PIL import Image

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
    img.show()
    return img

def create_image(base, dic): # Создает бинарный вектор образа
  a = np.array([])
  for i in base:
    a = np.append(a, dic[i])
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

simvols = {"#": 1,
           "_": -1}
simvols_revers = {1:'#',
                  -1:'_'}

t = "##########"\
    "##########"\
    "____##____"\
    "____##____"\
    "____##____"\
    "____##____"\
    "____##____"\
    "____##____"\
    "____##____"\
    "____##____"

n = "##______##"\
    "##______##"\
    "##______##"\
    "##______##"\
    "##########"\
    "##########"\
    "##______##"\
    "##______##"\
    "##______##"\
    "##______##"

k = "##______##"\
    "##_____##_"\
    "##____##__"\
    "##__##____"\
    "####______"\
    "####______"\
    "##__##____"\
    "##____##__"\
    "##_____##_"\
    "##______##"

images = np.array([create_image(t, simvols), 
                  create_image(n, simvols), 
                  create_image(k, simvols)])

t1 = "#######_##"\
     "##_#######"\
     "____##____"\
     "____##____"\
     "____##____"\
     "___###____"\
     "____##____"\
     "____##__#_"\
     "____##____"\
     "____##____"

n1 = "##______##"\
     "###_____##"\
     "###______#"\
     "##______##"\
     "####_#####"\
     "#######_##"\
     "#___#___##"\
     "##_#___###"\
     "##______##"\
     "##______##"

k1 = "##______##"\
     "###____##_"\
     "##____####"\
     "##__###___"\
     "####___#__"\
     "#_##____#_"\
     "##__##____"\
     "##________"\
     "###____##_"\
     "##______##"

pa = "_#________"\
     "__________"\
     "__________"\
     "__________"\
     "__________"\
     "__________"\
     "_____#____"\
     "__________"\
     "#_________"\
     "_##_______"

signals = np.array([create_image(t1, simvols), 
                    create_image(n1, simvols), 
                    create_image(k1, simvols), 
                    create_image(pa, simvols)])

NEURONS_NUMBER = len(t) # 100 # количество нейронов
MAX_STEPS = 100 # максимальное кол-во итераций

h = Hopfild(NEURONS_NUMBER, MAX_STEPS)
h.remember(images)

answer = ''
for signal in signals:
  res = h.associations(signal)
  print_images(signal, res, simvols_revers, 10)
  draw_image_from_array(signal, 10, 10)
  draw_image_from_array(res, 10, 10)
  input('Нажмите Enter для продолжения...') # ожидание ввода