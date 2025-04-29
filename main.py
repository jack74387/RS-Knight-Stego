import argparse
from stegano.encoder import StegoEncoder
from stegano.decoder import StegoDecoder

def main():
    parser = argparse.ArgumentParser(description="RS Knight Stego")
    subparsers = parser.add_subparsers(dest='command')

    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('-i', '--input', required=True, help='Input image')
    encode_parser.add_argument('-d', '--data', required=True, help='Data file to hide')
    encode_parser.add_argument('-o', '--output', required=True, help='Output stego image')
    encode_parser.add_argument('-s', '--seed', type=int, default=42, help='Seed for knight tour')
    encode_parser.add_argument('--rs', type=int, default=3, help='Number of RS parity bytes')

    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('-i', '--input', required=True, help='Input stego image')
    decode_parser.add_argument('-o', '--output', required=True, help='Output recovered file')
    decode_parser.add_argument('-s', '--seed', type=int, default=42, help='Seed for knight tour')
    decode_parser.add_argument('--rs', type=int, default=3, help='Number of RS parity bytes')

    args = parser.parse_args()

    if args.command == 'encode':
        with open(args.data, 'rb') as f:
            data = f.read()
        encoder = StegoEncoder(seed=args.seed, rs_nsym=args.rs)
        encoder.encode_image(args.input, args.output, data)
    elif args.command == 'decode':
        decoder = StegoDecoder(seed=args.seed, rs_nsym=args.rs)
        recovered = decoder.decode_image(args.input)
        with open(args.output, 'wb') as f:
            f.write(recovered)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
