using DrumsFinder.Base;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class Partition : ObservableObject
    {
        public ObservableCollection<Measure> Measures { get; set; }

        private int _tempo;
        public int Tempo
        {
            get
            {
                return _tempo;
            }
            set
            {
                if (value > 0 && value < 1000)
                {
                    _tempo = value;
                    foreach( Measure measure in Measures)
                        measure.RaisePropertyChangedEvent("Duration");
                }
            }
        }

        private int _upperTimeSig, _lowerTimeSig;
        public string TimeSignature {
            get
            {
                return _upperTimeSig + "/" + _lowerTimeSig;
            }
            set
            {
                Regex rgx = new Regex("^[1-9][0-9]?/(1|2|4|8|16|32)$");

                if (rgx.IsMatch(value))
                {
                    string[] result = value.Split('/');
                    _upperTimeSig = int.Parse(result[0]);
                    _lowerTimeSig = int.Parse(result[1]);
                }
            }
        }

        public Partition()
        {
            Measures = new ObservableCollection<Measure>();
            for(int i = 0 ; i < 15; i++)
                Measures.Add(new Measure(this));


            Tempo = 120;
            TimeSignature = "4/4";
        }

        public double GetMeasureTime()
        {
            double Length = _upperTimeSig * 1 / _lowerTimeSig;

            return Length / (Tempo * 4);
        }

        //TODO enable playing drums sample in function of the partition
        public void Play(TimeSpan Start)
        {
            //TimeSpan total = TimeSpan.Zero;
            //foreach(Measure measure in Measures)
            //{
            //    if (total >= Start)
            //    {
            //        foreach(Note note in measure.Notes)
            //        {
            //            if(total >= Start)
            //            {

            //            }
            //            total.Add(TimeSpan.FromSeconds(note.Duration());
            //        }
            //    }
            //    total.Add(TimeSpan.FromSeconds(measure.Duration());
            //}
        }
    }
}
