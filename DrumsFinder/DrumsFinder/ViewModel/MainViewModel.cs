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
    class MainViewModel : ObservableObject
    {
        // TODO put this inside a class ?
        private SampleAggregator _sampleAggregator;

        public float[] Wave
        {
            get
            {
                if (_sampleAggregator == null)
                    return new float[0];

                TimeSpan before = CurrentTime.Value;

                float[] samples = new float[_sampleAggregator.SamplesNumber];
                _sampleAggregator.Read(samples, 0, _sampleAggregator.SamplesNumber);

                CurrentTime = before;

                return samples;
            }
        }

        public bool MusicLoaded
        {
            get
            {
                return _sampleAggregator != null;
            }
        }

        public TimeSpan? CurrentTime
        {
            get
            {
                if (_sampleAggregator != null)
                    return _sampleAggregator.CurrentTime;
                else
                    return null;
            }
            set
            {

                if (_sampleAggregator != null)
                {
                    _sampleAggregator.CurrentTime = value.Value;
                }
            }
        }

        public TimeSpan? TotalTime
        {
            get
            {
                if (_sampleAggregator != null)
                    return _sampleAggregator.TotalTime;
                else
                    return null;
            }
        }


        private TimeSpan? _startSelect;
        public TimeSpan? StartSelect
        {
            get { return _startSelect; }
            set
            {
                _startSelect = value;
                CurrentTime = value;
            }
        }


        private TimeSpan? _endSelect;
        public TimeSpan? EndSelect
        {
            get { return _endSelect; }
            set { _endSelect = value; }
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

                if (_sampleAggregator != null)
                    _sampleAggregator.Volume = value;

            }
        }

        public bool Playing { get; set; }

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
                if (_sampleAggregator != null)
                {
                    _sampleAggregator.SampleRead -= sampleAggregator_SampleRead;
                    AudioPlayBack.MixingSampleProvider.RemoveMixerInput(_sampleAggregator as ISampleProvider);
                }

                //TODO try catch here ?
                try
                {
                    _sampleAggregator = AudioPlayBack.LoadSound(dlg.FileName);
                    _sampleAggregator.SampleRead += sampleAggregator_SampleRead;

                    this.Playing = false;
                    this.Volume = Volume;
                    RaisePropertyChangedEvent("Wave");
                    RaisePropertyChangedEvent("CurrentTime");
                    RaisePropertyChangedEvent("TotalTime");
                    RaisePropertyChangedEvent("MusicLoaded");
                    //_musicFile.audioFileReader.
                }
                catch (Exception e)
                {
                    Console.WriteLine("Bad input file " + e);
                }
            }
        }


        //New action
        public ICommand PlayPause
        {
            get
            {
                return new RelayCommand(
                    delegate()
                    {
                        // TODO Enable playing and pausing (as well as changing the time) of the music 
                        if (this.Playing)
                        {
                            AudioPlayBack.MixingSampleProvider.RemoveMixerInput(_sampleAggregator as ISampleProvider);
                            this.Playing = false;
                        }
                        else
                        {
                            AudioPlayBack.MixingSampleProvider.AddMixerInput(_sampleAggregator as IWaveProvider);
                            this.Playing = true;
                        }
                    },
                    delegate() { return _sampleAggregator != null || Partition != null; });
            }
        }

        void sampleAggregator_SampleRead(object sender, EventArgs e)
        {
            if (CurrentTime > EndSelect)
                CurrentTime = StartSelect;

            RaisePropertyChangedEvent("CurrentTime");
        }
    }
}
