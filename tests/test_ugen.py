from unittest import TestCase
from pya import *
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)


class TestUgen(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sine(self):
        sine = Ugen().sine(freq=200, amp=0.5, dur=1.0, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, sine.sr)
        self.assertAlmostEqual(0.5, np.max(sine.sig), places=6)
        self.assertEqual((44100 // 2, 2), sine.sig.shape)
        
        sine = Ugen().sine(freq=200, amp=0.5, n_rows= 44100 // 2, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, sine.sr)
        self.assertAlmostEqual(0.5, np.max(sine.sig), places=6)
        self.assertEqual((44100 // 2, 2), sine.sig.shape)

    def test_cos(self):
        cos = Ugen().cos(freq=200, amp=0.5, dur=1.0, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, cos.sr)
        self.assertAlmostEqual(0.5, np.max(cos.sig), places=6)
        self.assertEqual((44100 // 2, 2), cos.sig.shape)
        cos = Ugen().cos(freq=200, amp=0.5, n_rows=44100 // 2, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, cos.sr)
        self.assertAlmostEqual(0.5, np.max(cos.sig), places=6)
        self.assertEqual((44100 // 2, 2), cos.sig.shape)

    def test_square(self):
        square = Ugen().square(freq=200, amp=0.5, dur=1.0, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, square.sr)
        self.assertAlmostEqual(0.5, np.max(square.sig), places=6)
        self.assertEqual((44100 // 2, 2), square.sig.shape)

    def test_sawooth(self):
        saw = Ugen().sawtooth(freq=200, amp=0.5, dur=1, sr=44100 // 2, channels=2)
        self.assertEqual(44100 // 2, saw.sr)
        self.assertAlmostEqual(0.5, np.max(saw.sig), places=6)
        self.assertEqual((44100 // 2, 2), saw.sig.shape)

    def test_noise(self):
        white = Ugen().noise(type="white", amp=0.2, dur=1.0, sr=1000, cn=['white'], label='white_noise')
        pink = Ugen().noise(type="pink")
        self.assertEqual(white.sr, 1000)
        self.assertAlmostEqual(np.max(white.sig), 0.2, places=3)
        self.assertAlmostEqual(white.get_duration(), 1.0, places=7)
        self.assertEqual(white.cn, ['white'])
        self.assertEqual(white.label, 'white_noise')
        white_2ch = Ugen().noise(type="pink", channels=2)
        self.assertEqual(white_2ch.channels, 2)
        
    def test_dur_n_rows_exception(self):
        # An exception should be raised if both dur and n_rows are define. 
        with self.assertRaises(AttributeError):
            asig = Ugen().sine(dur=1., n_rows=400)
        