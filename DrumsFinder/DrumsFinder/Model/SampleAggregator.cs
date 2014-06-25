using NAudio.Wave;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class SampleAggregator : IWaveProvider
    {
        private IWaveProvider _source;
        public event EventHandler<EventArgs> SampleRead;

        public SampleAggregator(IWaveProvider Source)
        {
            _source = Source;

        }

        public WaveFormat WaveFormat
        {
            get { return _source.WaveFormat; }
        }

        public int Read(byte[] buffer, int offset, int count)
        {
            if (SampleRead != null)
            {
                SampleRead(this, new EventArgs());
            }

            return _source.Read(buffer, offset, count);
        }
    }
}
