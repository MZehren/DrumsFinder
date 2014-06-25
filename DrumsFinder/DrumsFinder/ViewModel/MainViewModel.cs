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
        private Point[] _wave;
        public Point[] Wave
        {
            get
            {
                if (_wave == null || _wave.Length == 0)
                {
                    Wave = _musicFile.GetWave(50000, 0, Int32.MaxValue);
                }
                return _wave;
            }

            private set
            {
                if (value == null)
                    _wave = new Point[0];
                else
                    _wave = value;
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
                    return _musicFile.audioFileReader.CurrentTime;
                else
                    return new TimeSpan();
            }
            set
            {

                if (_musicFile != null)
                {
                    _musicFile.audioFileReader.CurrentTime = value;
                   
                }
            }
        }

        public TimeSpan TotalTime
        {
            get
            {
                if (_musicFile != null)
                    return _musicFile.audioFileReader.TotalTime;
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
                    _musicFile.audioFileReader.Volume = value;

            }
        }


        public MainViewModel()
        {
            SetMusicFile = new RelayCommand(PerformSetMusicFile);

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
                    //OnPropertyChanged("Wave");
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
                        
                        if (_musicFile.waveOutDevice.PlaybackState != PlaybackState.Playing)
                        {
                            _musicFile.Play();
                            _musicFile.sampleAggregator.SampleRead += sampleAggregator_SampleRead;
                        }
                        else
                        {
                            _musicFile.Pause();
                            _musicFile.sampleAggregator.SampleRead -= sampleAggregator_SampleRead;
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
