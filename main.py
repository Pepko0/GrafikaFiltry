from PIL import Image
from mean_filter import MeanFilter
from median_filter import MedianFilter
from sobel_filter import SobelFilter
from binarize_filter import BinarizeFilter
from dilation_filter import DilationFilter
from erosion_filter import ErosionFilter




def load_image(path):
    """
    Wczytuje obraz, zamienia na skalę szarości
    i zwraca:
    - data: tablica 2D pikseli (0..255)
    - w: szerokość
    - h: wysokość
    """
    img = Image.open(path)     # otwarcie pliku
    img = img.convert("L")     # "L" = grayscale (1 kanał)
    w, h = img.size            # rozmiar obrazu

    pixels = list(img.getdata())  # lista wszystkich pikseli 1D
    data = [pixels[i*w:(i+1)*w] for i in range(h)]  # zamiana na 2D

    return data, w, h


def save_image(data, w, h, path):
    """
    Zapisuje tablicę 2D pikseli jako obraz.
    """
    img = Image.new("L", (w, h))   # tworzymy pusty obraz grayscale

    flat = [v for row in data for v in row]  # spłaszczenie 2D -> 1D
    img.putdata(flat)  # wrzucenie pikseli
    img.save(path)     # zapis do pliku

def choose_structuring_element():
    """
    choose_structuring_element
    Co robi: pozwala wybrać gotowy element strukturyzujący z listy.
    Przyjmuje:
        nic
    Zwraca:
        struct_elem (list[list[int]]): wybrany SE 0/1
    """
    print("\nWybierz element strukturyzujący:")
    print("1 - kwadrat 3x3")
    print("2 - krzyż 3x3")
    print("3 - kwadrat 5x5")
    print("4 - pozioma linia 1x5")
    print("5 - pionowa linia 5x1")

    choice = int(input("Twój wybór: "))

    if choice == 1:
        return [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]
    elif choice == 2:
        return [
            [0,1,0],
            [1,1,1],
            [0,1,0]
        ]
    elif choice == 3:
        return [
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1]
        ]
    elif choice == 4:
        return [[1,1,1,1,1]]  
    elif choice == 5:
        return [
            [1],
            [1],
            [1],
            [1],
            [1]
        ]  
    else:
        print("Nie ma takiej opcji, biorę domyślny 3x3.")
        return [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]


def main():
    data, w, h = load_image("images/test2.PNG")

    # mean
    mean_filter = MeanFilter(kernel_size=3)
    smooth_data = mean_filter.apply(data)
    save_image(smooth_data, w, h, "images/test_mean.png")

    # median
    median_filter = MedianFilter(kernel_size=3)
    median_data = median_filter.apply(data)
    save_image(median_data, w, h, "images/test_median.png")

    # sobel
    sobel_filter = SobelFilter()
    sobel_data = sobel_filter.apply(data)
    save_image(sobel_data, w, h, "images/test_sobel.png")

    # 1) binaryzacja (próg możesz zmienić)
    bin_filter = BinarizeFilter(threshold=128)
    bin_data = bin_filter.apply(data)
    save_image(bin_data, w, h, "images/test_binary.png")

    # 2) element strukturyzujący od użytkownika
    struct_elem = choose_structuring_element()
    dilation = DilationFilter(struct_elem)
    dilated_data = dilation.apply(bin_data)
    save_image(dilated_data, w, h, "images/test_dilate.png")

    # erozja
    erosion = ErosionFilter(struct_elem)
    eroded_data = erosion.apply(bin_data)
    save_image(eroded_data, w, h, "images/test_erode.png")


    print("Już w końcu się zrobiło")


if __name__ == "__main__":
    main()
