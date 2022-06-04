from enums.color import Color
from enums.error_collection_level import ErrorCollectionLevel
from rmqr.rmqr import rMQR
from rmqr.rmqr import DataTooLongError
from rmqr.data_capacities import data_capacities
from encoder.byte_encoder import ByteEncoder
from qr_image import QRImage


def select_version(data, error_collection_level):
    data_length = ByteEncoder.length(data)
    ok_versions = []
    for qr_version, capacity in data_capacities.items():
        if data_length <= capacity['Byte'][error_collection_level]:
            ok_versions.append({
                'version': qr_version,
                'diff': capacity['Byte'][error_collection_level] - data_length
            })
            print(f"ok: {qr_version}")

    if len(ok_versions) == 0:
        raise DataTooLongError("The data is too long.")

    # とりあえず容量のあまりが最も少なくなるものを選ぶ
    # TODO: 選び方をパラメータで変えられるようにしたい
    selected = sorted(ok_versions, key=lambda x: x['diff'])[0]
    return selected['version']


def make_qr(data, version, error_collection_level):
    qr = rMQR(version, error_collection_level)
    qr.make(data)
    return qr


def main():
    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. orem ipsum dolor sit amet, consectetur adipi"
    error_collection_level = ErrorCollectionLevel.M
    version = select_version(data, error_collection_level)
    print(f"selected: {version}")
    qr = make_qr(data, version, error_collection_level)
    qr.dump()

    image = QRImage(qr)
    image.show()
    image.save("output/my_qr.png")


if __name__ == '__main__':
    main()
