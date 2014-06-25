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
        //public BlockAlignReductionStream blockAlignReductionStream;
        //public DirectSoundOut directSoundOut;
        //public WaveStream waveStream;
        //public MeteringSampleProvider MeteringSampleProvider;

        public AudioFileReader audioFileReader;
        public IWavePlayer waveOutDevice;
        public SampleAggregator sampleAggregator;
        private int _bytesPerSample;

        public MusicFile(string fileName)
        {
   
               
                audioFileReader = new AudioFileReader(fileName);
                sampleAggregator = new SampleAggregator(audioFileReader);
                waveOutDevice = new WaveOut();
                waveOutDevice.Init(sampleAggregator);

                //if (fileName.EndsWith(".mp3"))
                //{

                //    waveStream = WaveFormatConversionStream.CreatePcmStream(new Mp3FileReader(fileName));

                //}
                //else if (fileName.EndsWith(".wav"))
                //{
                //    waveStream = new WaveChannel32(new NAudio.Wave.WaveFileReader(fileName));

                //}
                //else
                //{
                //    throw new InvalidOperationException("Unsupported extension");
                //}

                //blockAlignReductionStream = new BlockAlignReductionStream(waveStream);
                //directSoundOut = new DirectSoundOut();
                //meteringSampleProvider = new MeteringSampleProvider(new WaveChannel32(waveStream));
                //directSoundOut.Init(blockAlignReductionStream);

                _bytesPerSample = (audioFileReader.WaveFormat.BitsPerSample / 8) * audioFileReader.WaveFormat.Channels;
            
            }

        public void Play()
        {
            waveOutDevice.Play();

        }

        public void Pause()
        {
            waveOutDevice.Pause();
        }

        public void Stop()
        {
            waveOutDevice.Stop();
        }

        private void _wavDispose()
        {
            if (waveOutDevice != null)
            {
                if (waveOutDevice.PlaybackState == PlaybackState.Playing)
                    waveOutDevice.Stop();
                waveOutDevice.Dispose();
                waveOutDevice = null;
            }
            if (audioFileReader != null)
            {
                audioFileReader.Dispose();
                audioFileReader = null;
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
