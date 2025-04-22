import argparse
from PIL import Image

# 默认字符集：从密到疏
DEFAULT_CHARS = "@%#*+=-:. "


def convert_image_to_ascii(image_path, output_file=None, width=100, chars=DEFAULT_CHARS, color=True):
    try:
        img = Image.open(image_path)
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.55)
        img = img.resize((width, new_height))
        # 因为终端比较长 所以要重置一下高度

        if color:
            img = img.convert("RGB")
        else:
            img = img.convert("L")

        ascii_art = ""

        for y in range(new_height):
            for x in range(width):
                if color:
                    r, g, b = img.getpixel((x, y))
                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # ITU-R BT.601标准
                    char = chars[min(gray * len(chars) // 256, len(chars) - 1)]
                    ascii_art += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                else:
                    gray = img.getpixel((x, y))
                    char = chars[min(gray * len(chars) // 256, len(chars) - 1)]
                    ascii_art += char
            ascii_art += "\n"

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(ascii_art)
            print(f"字符画已保存到 {output_file}")
        else:
            print(ascii_art)

    except Exception as e:
        print(f"错误: {str(e)}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将图片转换为字符画（支持彩色）")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出文件（默认为控制台显示）")
    parser.add_argument("-w", "--width", type=int, default=100, help="输出宽度（默认100字符）")
    parser.add_argument("-c", "--chars", default=DEFAULT_CHARS,
                        help=f"自定义字符集（默认：'{DEFAULT_CHARS}'）")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出（默认启用）")

    args = parser.parse_args()

    if len(args.chars) < 2:
        print("错误：字符集至少需要2个字符")
        exit(1)

    convert_image_to_ascii(
        args.image,
        output_file=args.output,
        width=args.width,
        chars=args.chars,
        color=not args.no_color
    )