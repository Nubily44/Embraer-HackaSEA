import cv2
import os


input_image_folder = '/home/ma-u2204/Documents/Programas/Python/Embraer'

output_video_file = 'video_saida.mp4'

fps = 30

image_files = sorted([os.path.join(input_image_folder, f) for f in os.listdir(input_image_folder) if f.endswith('.png')])

if len(image_files) == 0:
    print("Nenhuma imagem encontrada no diretório de entrada.")
    exit()

first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para o formato MP4
out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

image_files.sort()

for image_file in image_files:
    frame = cv2.imread(image_file)
    out.write(frame)


out.release()

print(f"Vídeo '{output_video_file}' criado com sucesso.")

