using DrumsFinder.Base;
using DrumsFinder.Model;
using NAudio.Wave;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;

namespace DrumsFinder.ViewModel
{
    class MainViewModel : ViewModelBase
    {
        private MusicFile _musicFile;

        public float[] Wave
        {
            get
            {
                if (_musicFile.AudioFileReader == null)
                    return null;

                TimeSpan before = CurrentTime;

                float[] samples = new float[_musicFile.AudioFileReader.SamplesNumber];
                _musicFile.AudioFileReader.Read(samples, 0, _musicFile.AudioFileReader.SamplesNumber);
               
                CurrentTime = before;

                return samples;
            }
        }


        public bool MusicLoaded
        {
            get
            {
                return _musicFile != null;
            }
        }

        public TimeSpan CurrentTime
        {
            get
            {
                if (_musicFile != null)
                    return _musicFile.AudioFileReader.CurrentTime;
                else
                    return new TimeSpan();
            }
            set
            {

                if (_musicFile != null)
                {
                    _musicFile.AudioFileReader.CurrentTime = value;
                   
                }
            }
        }

        public TimeSpan TotalTime
        {
            get
            {
                if (_musicFile != null)
                    return _musicFile.AudioFileReader.TotalTime;
                else
                    return new TimeSpan();
            }
        }

        private float _volume;
        public float Volume
        {
            get
            {
                return _volume;
            }
            set
            {
                if (value > 1 || value < 0)
                    return;

                _volume = value;

                if (_musicFile != null)
                    _musicFile.AudioFileReader.Volume = value;

            }
        }

        public Partition Partition { get; set; }

        public MainViewModel()
        {
            SetMusicFile = new RelayCommand(PerformSetMusicFile);
            Partition = new Partition();
            
            // dragView = new RelayCommand<int>(PerformDragView);
        }

        //New action
        public ICommand SetMusicFile { get; private set; }

        private void PerformSetMusicFile()
        {
            //Open File
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            // dlg.DefaultExt = ".txt";
            // dlg.Filter = "Audio File (*.mp3;*.wav)|*.mp3;*.wav";
            Nullable<bool> result = dlg.ShowDialog();

            if (result == true)
            {
                if (_musicFile != null)
                {
                    _musicFile.Stop();
                    _musicFile = null;
                }

                try
                {
                    _musicFile = new MusicFile(dlg.FileName);

                    this.Volume = Volume;
                    OnPropertyChanged("Wave");
                    OnPropertyChanged("CurrentTime");
                    OnPropertyChanged("TotalTime");
                    OnPropertyChanged("MusicLoaded");
                    //_musicFile.audioFileReader.
                }
                catch (Exception)
                {
                    Console.WriteLine("Bad input file");
                }
            }
        }


        //New action
        public ICommand PlayPause
        {
            get
            {
                return new RelayCommand(
                    delegate() { 
                        
                        if (_musicFile.WaveOutDevice.PlaybackState != PlaybackState.Playing)
                        {
                            _musicFile.Play();
                            _musicFile.AudioFileReader.SampleRead += sampleAggregator_SampleRead;
                        }
                        else
                        {
                            _musicFile.Pause();
                            _musicFile.AudioFileReader.SampleRead -= sampleAggregator_SampleRead;
                        }
                    },
                    delegate() { return _musicFile != null; });
            }
        }

        void sampleAggregator_SampleRead(object sender, EventArgs e)
        {
            OnPropertyChanged("CurrentTime");
        }


        //New action
        //public ICommand dragView { get; private set; }

        //private void PerformDragView(int x)
        //{
        //    Wave = _musicFile.GetWave(x, 0, Int32.MaxValue);
        //    OnPropertyChanged("Wave");
        //}
    }
}
