using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;

namespace DrumsFinder.View.Converter
{
    [ValueConversion(typeof(float[]), typeof(Geometry))]
    class FloatsToPathConverter : IValueConverter
    {
        #region IValueConverter Members

        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            float[] points = (float[])value;
            if (points.Length > 0)
            {
                List<LineSegment> segments = new List<LineSegment>();
                int j = 0;
                for (int i = 1; i < points.Length; i+=44100)
                {
                    j++;
                    segments.Add(new LineSegment(new Point(j, points[i]), true));
                }
                PathFigure figure = new PathFigure(new Point(), segments, false); //true if closed
                PathGeometry geometry = new PathGeometry();
                geometry.Figures.Add(figure);
                return geometry;
            }
            else
            {
                return null;
            }
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotSupportedException();
        }

        #endregion
    }
}
