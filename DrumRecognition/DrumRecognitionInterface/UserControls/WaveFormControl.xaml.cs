
using NAudio.Wave;
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



namespace DrumRecognitionInterface.UserControls
{
    /// <summary>
    /// Control permettant l'affichage d'un WaveForm
    /// </summary>
    public partial class WaveFormControl : UserControl
    {
        private WaveStream _waveStream;
        private int _bytesPerSample;
        private int _samplesPerPixel = 50;

        public int SamplesPerPixel { 
            get { return _samplesPerPixel; } 
            private set { if (value < 1) _samplesPerPixel = 1; else _samplesPerPixel = value; } 
        }

        private Pen _pen = new Pen(Brushes.Black, 1);
        public WaveFormControl()
        {
            InitializeComponent();
        }
        
        /// <summary>
        /// sets the associated wavestream
        /// </summary>
        public WaveStream WaveStream
        {
            get
            {
                return _waveStream;
            }
            set
            {
                _waveStream = value;
                if (_waveStream != null)
                {
                    _bytesPerSample = (_waveStream.WaveFormat.BitsPerSample / 8) * _waveStream.WaveFormat.Channels;
                }
                this.InvalidateVisual();
            }
        }


        protected override void OnRender(DrawingContext dc)
        {
            base.OnRender(dc);               
            
            if (_waveStream != null)
            {
                _waveStream.Position = 0;
                _waveStream.Skip(11);
                byte[] waveData = new byte[_samplesPerPixel*_bytesPerSample];
                int bytesRead;
                
                //for each pixel in the width
                for (float x = 0; x < this.ActualWidth; x += 1)
                {
                    short low = 0;
                    short high = 0;
                    bytesRead = _waveStream.Read(waveData, 0, _samplesPerPixel * _bytesPerSample);
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


                    dc.DrawLine(_pen, new Point(x, this.ActualHeight * lowPercent), new Point(x, this.ActualHeight * highPercent));
               
                }
     
            }
            
         
        }

        private void UserControl_MouseWheel_1(object sender, MouseWheelEventArgs e)
        {
            SamplesPerPixel -= e.Delta / 5;
            this.InvalidateVisual();
        }


        private void UserControl_MouseMove_1(object sender, MouseEventArgs e)
        {

        }

        private void UserControl_MouseDown_1(object sender, MouseButtonEventArgs e)
        {

        }



    }
}
