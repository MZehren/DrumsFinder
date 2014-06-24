using DrumsFinder.Base;
using DrumsFinder.Model;
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
            dlg.DefaultExt = ".txt";
            dlg.Filter = "Audio File (*.mp3;*.wav)|*.mp3;*.wav";
            Nullable<bool> result = dlg.ShowDialog();

            if (result == true)
            {
                if (_musicFile != null)
                {
                    _musicFile.Stop();
                    _wave = null;
                }

                _musicFile = new MusicFile(dlg.FileName);

                OnPropertyChanged("Wave");
            }
        }

        //New action
        public ICommand PlayPause
        {
            get
            {
                return new RelayCommand(
                    delegate() { _musicFile.PlayPause(); },
                    delegate() { return _musicFile != null; });
            }
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
