from rmqrcode import console

import pytest


class TestConsoleEmptyData:
    def test_empty_data_exits_cleanly(self, monkeypatch, capsys, tmp_path):
        output = tmp_path / "out.png"
        monkeypatch.setattr("sys.argv", ["rmqr", "", str(output)])
        with pytest.raises(SystemExit) as excinfo:
            console.main()
        assert excinfo.value.code == 1
        _, err = capsys.readouterr()
        assert "Traceback" not in err
