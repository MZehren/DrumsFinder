using DrumsFinder.Base;
using NAudio.Wave;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace DrumsFinder.Model
{
    public class MusicFile : IDisposable
    {
        private BlockAlignReductionStream blockAlignReductionStream;
        public DirectSoundOut directSoundOut;
        private WaveStream _waveStream;
        private int _bytesPerSample;

        public MusicFile(string fileName)
        {
            if (fileName.EndsWith(".mp3"))
            {
                _waveStream = WaveFormatConversionStream.CreatePcmStream(new Mp3FileReader(fileName));

            }
            else if (fileName.EndsWith(".wav"))
            {
                _waveStream = new WaveChannel32(new NAudio.Wave.WaveFileReader(fileName));

            }
            else
            {
                throw new InvalidOperationException("Unsupported extension");
            }

            blockAlignReductionStream = new BlockAlignReductionStream(_waveStream);
            directSoundOut = new DirectSoundOut();
            directSoundOut.Init(blockAlignReductionStream);
            _bytesPerSample = (_waveStream.WaveFormat.BitsPerSample / 8) * _waveStream.WaveFormat.Channels;
        }

        public void Play()
        {
            directSoundOut.Play();
        }

        public void Pause()
        {
            directSoundOut.Pause();
        }

        public void PlayPause()
        {
            if (directSoundOut.PlaybackState != PlaybackState.Playing)
                Play();
            else
                Pause();

        }

        public void Stop()
        {
            directSoundOut.Stop();
        }

        private void _wavDispose()
        {
            if (directSoundOut != null)
            {
                if (directSoundOut.PlaybackState == PlaybackState.Playing)
                    directSoundOut.Stop();
                directSoundOut.Dispose();
                directSoundOut = null;
            }
            if (blockAlignReductionStream != null)
            {
                blockAlignReductionStream.Dispose();
                blockAlignReductionStream = null;
            }
        }

        void IDisposable.Dispose()
        {
            _wavDispose();
        }

        internal Point[] GetWave(int samplesPerPixel, int xMin, int xMax)
        {
            if (_waveStream != null)
            {
                _waveStream.Position = xMin;

                byte[] waveData = new byte[samplesPerPixel * _bytesPerSample];
                int bytesRead;
                List<Point> result = new List<Point>();

                while (_waveStream.Position < _waveStream.Length || _waveStream.Position < xMax)
                {
                    short low = 0;
                    short high = 0;
                    bytesRead = _waveStream.Read(waveData, 0, samplesPerPixel * _bytesPerSample);
                    if (bytesRead == 0)
                        break;
                    for (int n = 0; n < bytesRead; n += 2)
                    {
                        short sample = BitConverter.ToInt16(waveData, n);
                        if (sample < low) low = sample;
                        if (sample > high) high = sample;
                    }
                    float lowPercent = ((((float)low) - short.MinValue) / ushort.MaxValue);
                    float highPercent = ((((float)high) - short.MinValue) / ushort.MaxValue);

                    result.Add(new Point(_waveStream.Position, lowPercent));
                    result.Add(new Point(_waveStream.Position, highPercent));

                }
                return result.ToArray();
            }
            else
                return null;
        }
    }
}
