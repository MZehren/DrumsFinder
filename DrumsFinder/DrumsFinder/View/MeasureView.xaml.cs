using DrumsFinder.Model;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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

namespace DrumsFinder.View
{
    /// <summary>
    /// Logique d'interaction pour MainView.xaml
    /// </summary>
    public partial class MeasureView : UserControl
    {
        //public Measure Measure {
        //    get { return (Measure)GetValue(MeasureProperty); }
        //    set { SetValue(MeasureProperty, value); }
        //}
        //public static readonly DependencyProperty MeasureProperty = DependencyProperty.Register(
        //"Measure", typeof(Measure), typeof(MeasureView), null);

        public int UpperTimeSig
        {
            get { return (int)GetValue(UpperTimeSigProperty); }
            set { SetValue(UpperTimeSigProperty, value); }
        }
        public static readonly DependencyProperty UpperTimeSigProperty = DependencyProperty.Register(
        "Measure", typeof(int), typeof(MeasureView), null);

        public MeasureView()
        {
            InitializeComponent();
        }

    }
}
