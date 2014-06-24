using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using NAudio.Wave;
using NAudio.Wave.SampleProviders;

namespace DrumRecognitionInterface
{
    /// <summary>
    /// Logique d'interaction pour MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private BlockAlignReductionStream blockAlignReductionStream;
        private DirectSoundOut directSoundOut;
        private WaveStream waveStream;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            //Open File
            Microsoft.Win32.OpenFileDialog dlg = new Microsoft.Win32.OpenFileDialog();
            dlg.DefaultExt = ".txt";
            dlg.Filter = "Audio File (*.mp3;*.wav)|*.mp3;*.wav";
            Nullable<bool> result = dlg.ShowDialog();

            if (result == true)
            {
                //to take care of an old opened file
                DisposeWave();

                string filename = dlg.FileName;
                if (filename.EndsWith(".mp3"))
                {
                    waveStream = WaveFormatConversionStream.CreatePcmStream(new Mp3FileReader(filename));
                  
                }
                else if (filename.EndsWith(".wav"))
                {
                    waveStream = new WaveChannel32(new NAudio.Wave.WaveFileReader(filename));
                   
                }
                else
                {
                    throw new InvalidOperationException("Unsupported extension");
                }


                this.waveFormControl.WaveStream = waveStream;
                /*
                blockAlignReductionStream = new BlockAlignReductionStream(waveStream);
                directSoundOut = new DirectSoundOut();
                directSoundOut.Init(blockAlignReductionStream);
                */
            }
        }

        private void DisposeWave()
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



    }
}
