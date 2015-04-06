using NAudio.Wave;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class SampleAggregator : AudioFileReader
    {
        public event EventHandler<EventArgs> SampleRead;

        public SampleAggregator(string fileName)
            : base(fileName)
        { }

        public int SamplesNumber
        {
            get
            {
                return (int)(this.WaveFormat.SampleRate * this.TotalTime.TotalSeconds);
            }
        }

        public int BytesPerSample
        {
            get
            {
                return (this.WaveFormat.BitsPerSample / 8) * this.WaveFormat.Channels;
            }
        }

        override public int Read(byte[] buffer, int offset, int count)
        {
            if (SampleRead != null)
            {
                SampleRead(this, new EventArgs());
            }

            return base.Read(buffer, offset, count);
        }

        //override public int Read(float[] buffer, int offset, int count)
        //{
        //    if (SampleRead != null)
        //    {
        //        SampleRead(this, new EventArgs());
        //    }

        //    return base.Read(buffer, offset, count);
        //}
    }
}
