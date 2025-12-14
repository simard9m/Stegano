#!/usr/bin/env python3

import argparse
from pathlib import Path

from PIL import Image


#longeur du message
TAILLE_ENTETE_BITS = 32

#Transforme les octets en bits
def _bytes_to_bits(data:bytes):
    for byte in data:
        #Vas cherche le bit le pluis fort au moins fort
        for i in range(7,-1,-1): 
            yield (byte >> i)&1
    
#Transofrome une liste de bits en bytes            
def _bits_to_bytes(bits):
    if len(bits) %8 !=0:
        raise ValueError("Le nombres de bits n'est pas un multiple de 8")
    out = bytearray()
    for i in range(0,len(bits),8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)

#Remplace le bit de poids le plus faible
def _set_lsb(value:int,bit:int)->int:
    return (value & ~1) | (bit & 1)

def cacher_secret(chemin_input:Path,chemin_output:Path,secret:str):
    #charger l'image et convertir en rgb et getr les tuiple rgb ainsi que la taille de l<img
    img = Image.open(chemin_input).convert("RGBA")
    largeur,hauteur = img.size
    pixels = list(img.getdata()) 
    
    #Encodage messaage
    secret_bytes = secret.encode("utf-8")
    secret_longeur = len(secret_bytes)
    
    #Encodage de la longeur du message sur 32 bitsd
    longeur_bytes = secret_longeur.to_bytes(4,byteorder="big")
    data_a_rentrer = longeur_bytes + secret_bytes
    
    bits_a_rentrer = list(_bytes_to_bits(data_a_rentrer))
    nb_bits = len(bits_a_rentrer)
    
    #Capacite max = 1 bits par composante 
    capacite_bits = largeur *hauteur *3
    
    if nb_bits > capacite_bits:
        print("--> /!\\ The secret string exceeds the maximum length supported by the image.")
        return
    
    new_pixels = []
    bit_index = 0
    
    for (r, g, b, a) in pixels:
        if bit_index < nb_bits:
            r = _set_lsb(r, bits_a_rentrer[bit_index])
            bit_index += 1
        if bit_index < nb_bits:
            g = _set_lsb(g, bits_a_rentrer[bit_index])
            bit_index += 1
        if bit_index < nb_bits:
            b = _set_lsb(b, bits_a_rentrer[bit_index])
            bit_index += 1
            
        new_pixels.append((r, g, b, a))
        
    #creer la nouvelle image et sauvegarder
    new_img = Image.new("RGBA", (largeur, hauteur))
    new_img.putdata(new_pixels)
    #chemin_output.parent.mkdir(parents=True, exist_ok=True)
    new_img.save(chemin_output, format="PNG")
    print(f"Secret hidden successfully in '{chemin_output}'.")
    
def reveler_secret(image_path:Path):
    #meme chose on get l<image la mets en rgb get la size  et les pixels
    img = Image.open(image_path).convert("RGBA")
    largeur,hauteur = img.size
    pixels = list(img.getdata())

    bits = []
    
    #Lire toutes les LSB en ordre RGB
    for (r, g, b, a) in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)
        
    #Lire la longeur du  message 
    lenght_bits = bits[:TAILLE_ENTETE_BITS]
    lenght_bytes = _bits_to_bytes(lenght_bits)
    longeur_msg = int.from_bytes(lenght_bytes, byteorder="big")
    
    #lire les bits du message
    total_msg_bits = longeur_msg * 8
    debut = TAILLE_ENTETE_BITS
    fin = debut + total_msg_bits
    
    if fin > len(bits):
        raise ValueError("Impossible de reconstituer le message, l'image semble corrompue ou ne contient pas de secret valide.")
    
    message_bits = bits[debut:fin]
    message_bytes = _bits_to_bytes(message_bits)
    secret = message_bytes.decode("utf-8", errors="replace")
    
    print(f'--> secret message is: "{secret}"')

def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="stegano",
        description="Simple PNG LSB steganography CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sous-commande hide
    hide_parser = subparsers.add_parser("hide", help="Cacher un secret dans un PNG")
    hide_parser.add_argument("-i", "--input", required=True, help="Chemin vers une image png")
    hide_parser.add_argument("-o", "--output", required=True, help="Chemin vers l'output")
    hide_parser.add_argument("-s", "--secret", required=True, help="String secrete a cacher")

    # Sous-commande reveal
    reveal_parser = subparsers.add_parser("reveal", help="Reveler le secret d'une image PNG")
    reveal_parser.add_argument("image", help="Chemin vers une image qui contient un secret")

    return parser

def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.command == "hide":
        cacher_secret(Path(args.input), Path(args.output), args.secret)
    elif args.command == "reveal":
        reveler_secret(Path(args.image))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()