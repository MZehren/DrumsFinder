using DrumsFinder.Base;
using NAudio.Wave;
using NAudio.Wave.SampleProviders;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace DrumsFinder.Model
{
    /// <summary>
    /// Contains a MixingSampleProvider to read multiFiles at the same time (as indicated here http://mark-dot-net.blogspot.fr/2014/02/fire-and-forget-audio-playback-with.html)
    /// You have to load the file first, and then add it to be read whenever you want
    /// </summary>
    public static class AudioPlayBack
    {
        //public SampleAggregator AudioFileReader;
        public static IWavePlayer WaveOutDevice;
        public static MixingSampleProvider MixingSampleProvider;
        public static Dictionary<string, SampleAggregator> SampleAggregators;

        static AudioPlayBack()
        {
            int SampleRate = 44100, ChannelCount = 2;
            WaveOutDevice = new WaveOut();
            MixingSampleProvider = new MixingSampleProvider(WaveFormat.CreateIeeeFloatWaveFormat(SampleRate, ChannelCount));
            MixingSampleProvider.ReadFully = true;
            WaveOutDevice.Init(MixingSampleProvider);

            //loadind /Data/Samples files
            SampleAggregators = new Dictionary<string, SampleAggregator>();
            string path = "../../../../Data/Samples";
            if (Directory.Exists(path))
            {
                foreach (string file in Directory.EnumerateFiles(path))
                {            
                    LoadSound(file);
                }
            }

            WaveOutDevice.Play();
        }

        public static SampleAggregator LoadSound(string FileName)
        {
            SampleAggregator audioFileReader = new SampleAggregator(FileName);
            if (!audioFileReader.WaveFormat.Equals(MixingSampleProvider.WaveFormat))
            {
                try
                {
                    WaveFormatConversionStream str = new WaveFormatConversionStream(MixingSampleProvider.WaveFormat, audioFileReader);
                }
                catch (Exception)
                {
                    Console.WriteLine("Couldn't convert the file " + FileName + " to make it Readable");
                    return null;
                }
            }
            
            SampleAggregators.Add(Path.GetFileNameWithoutExtension(FileName), audioFileReader);
            return audioFileReader;
        }

        public static void AddSound(SampleAggregator SampleProvider)
        {
            MixingSampleProvider.AddMixerInput(SampleProvider as IWaveProvider);
        }

        public static void AddSound(string Name)
        {
            SampleAggregator sample;
            if (SampleAggregators.TryGetValue(Name, out sample))
            {
                sample.Position = 0;
                AddSound(sample);
            }
        }

        public static void AddSound(NoteKind Name)
        {
            foreach (string sampleName in Name.ToString().Split(','))
            {
                AddSound(sampleName);
            }
        }

        //private void _wavDispose()
        //{
        //    if (WaveOutDevice != null)
        //    {
        //        if (WaveOutDevice.PlaybackState == PlaybackState.Playing)
        //            WaveOutDevice.Stop();
        //        WaveOutDevice.Dispose();
        //        WaveOutDevice = null;
        //    }
        //    if (AudioFileReader != null)
        //    {
        //        AudioFileReader.Dispose();
        //        AudioFileReader = null;
        //    }
        //}

        //void IDisposable.Dispose()
        //{
        //    _wavDispose();
        //}


    }
}
