import time
from unittest import TestCase, skipUnless, mock
from pya import *
import numpy as np
import pyaudio

# check if we have an output device
has_output = False
try:
    pyaudio.PyAudio().get_default_output_device_info()
    has_output = True
except OSError:
    pass


class MockAudio(mock.MagicMock):
    channels_in = 1
    channels_out = 4

    def get_device_info_by_index(self, *args):
        return {'maxInputChannels': self.channels_in, 'maxOutputChannels': self.channels_out,
                'name': 'MockAudio', 'index': 42}


class TestPlay(TestCase):

    def setUp(self):
        self.sig = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))
        self.asine = Asig(self.sig, sr=44100, label="test_sine")
        self.asineWithName = Asig(self.sig, sr=44100, label="test_sine", cn=['sine'])
        # self.astereo = Asig("../examples/samples/stereoTest.wav", label='stereo', cn = ['l','r'])
        # self.asentence = Asig("../examples/samples/sentence.wav", label='sentence', cn = 'sen')
        self.sig2ch = np.repeat(self.sig, 2).reshape((44100, 2))
        self.astereo = Asig(self.sig2ch, sr=44100, label="stereo", cn=['l', 'r'])

    def tearDown(self):
        pass

    # @skipUnless(has_output, "PyAudio found no output device.")
    def test_mock_play(self):

        # Shift a mono signal to chan 4 should result in a 4 channels signals
        mock_audio = MockAudio()
        with mock.patch('pyaudio.PyAudio', return_value=mock_audio):
            s = Aserver()
            s.boot()
            assert mock_audio.open.called
            # since default AServer channel output is stereo we expect open to be called with
            # channels=2 
            self.assertEqual(mock_audio.open.call_args_list[0][1]["channels"], 2)
            d1 = np.linspace(0, 1, 44100)
            d2 = np.linspace(0, 1, 44100)
            asig = Asig(d1)
            s.play(asig)
            self.assertTrue(np.allclose(s.srv_asigs[0].sig, d2.reshape(44100, 1)))

        with mock.patch('pyaudio.PyAudio', return_value=mock_audio):
            s = Aserver(channels=6)
            s.boot()
            # AServer should reduce channels to 4 since MckAudio only pprovides 
            # 4 output channels
            assert mock_audio.open.call_count == 2
            self.assertEqual(mock_audio.open.call_args_list[1][1]["channels"], 4)
        with mock.patch('pyaudio.PyAudio', return_value=mock_audio): 
            s = Aserver(channels=6)   
            print(s)
            s.print_device_info()
            s.get_devices()
            # Set device is not tested. 
            # s.set_device(idx=1)
            # s.set_device(idx=1, reboot=True)

    @skipUnless(has_output, "PyAudio found no output device.")
    def test_play(self):
        s = Aserver()
        s.boot()
        self.asine.play(server=s)
        time.sleep(2)

    @skipUnless(has_output, "PyAudio found no output device.")   
    def test_stop(self):
        s = Aserver()
        s.boot()
        self.asine.play(server=s)
        s.stop()
        s.quit()

    def test_gain(self):
        result = (self.asine * 0.2).sig
        expected = self.asine.sig * 0.2
        self.assertTrue(np.allclose(result, expected))  # float32 should use allclose for more forgiving precision

        expected = self.sig * self.sig
        result = (self.asine * self.asine).sig
        self.assertTrue(np.allclose(result, expected))

    def test_resample(self):
        # This test currently only check if there is error running the code, but not whether resampling is correct
        result = self.asine.resample(target_sr=44100 // 2, rate=1, kind='linear')
        self.assertIsInstance(result, Asig)