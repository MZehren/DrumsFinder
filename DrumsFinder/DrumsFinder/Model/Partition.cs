using DrumsFinder.Base;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class Partition : ObservableObject
    {
        public ObservableCollection<Measure> Measures { get; set; }
        public int Tempo { get; set; }

        public Partition()
        {
            Measures = new ObservableCollection<Measure>();
            Measures.Add(new Measure());
            Measures.Add(new Measure());

            Tempo = 120;
        }
    }
}
