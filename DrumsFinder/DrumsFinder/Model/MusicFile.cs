using DrumsFinder.Base;
using NAudio.Wave;
using NAudio.Wave.SampleProviders;
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
        public SampleAggregator AudioFileReader;
        public IWavePlayer WaveOutDevice;



        public MusicFile(string fileName)
        {

            AudioFileReader = new SampleAggregator(fileName);
            WaveOutDevice = new WaveOut();
            WaveOutDevice.Init(AudioFileReader);

        }

        public void Play()
        {
            WaveOutDevice.Play();
        }

        public void Pause()
        {
            WaveOutDevice.Pause();
        }

        public void Stop()
        {
            WaveOutDevice.Stop();
        }

        private void _wavDispose()
        {
            if (WaveOutDevice != null)
            {
                if (WaveOutDevice.PlaybackState == PlaybackState.Playing)
                    WaveOutDevice.Stop();
                WaveOutDevice.Dispose();
                WaveOutDevice = null;
            }
            if (AudioFileReader != null)
            {
                AudioFileReader.Dispose();
                AudioFileReader = null;
            }
        }

        void IDisposable.Dispose()
        {
            _wavDispose();
        }

        internal Point[] GetWave(int samplesPerPixel, int xMin, int xMax)
        {
            //if (waveStream != null)
            //{
            //    waveStream.Position = xMin;

            //    byte[] waveData = new byte[samplesPerPixel * _bytesPerSample];
            //    int bytesRead;
            //    List<Point> result = new List<Point>();

            //    while (waveStream.Position < waveStream.Length || waveStream.Position < xMax)
            //    {
            //        short low = 0;
            //        short high = 0;
            //        bytesRead = waveStream.Read(waveData, 0, samplesPerPixel * _bytesPerSample);
            //        if (bytesRead == 0)
            //            break;
            //        for (int n = 0; n < bytesRead; n += 2)
            //        {
            //            short sample = BitConverter.ToInt16(waveData, n);
            //            if (sample < low) low = sample;
            //            if (sample > high) high = sample;
            //        }
            //        float lowPercent = ((((float)low) - short.MinValue) / ushort.MaxValue);
            //        float highPercent = ((((float)high) - short.MinValue) / ushort.MaxValue);

            //        result.Add(new Point(waveStream.Position, lowPercent));
            //        result.Add(new Point(waveStream.Position, highPercent));

            //    }
            //    return result.ToArray();
            //}
            //else
            return null;
        }
    }
}
