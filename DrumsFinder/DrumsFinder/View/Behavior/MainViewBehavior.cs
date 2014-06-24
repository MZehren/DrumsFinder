//using DrumsFinder.ViewModel;
//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
//using System.Windows;
//using System.Windows.Interactivity;
//using System.Windows.Shapes;

//namespace DrumsFinder.View.Behavior
//{
//    public class MainViewBehavior : Behavior<FrameworkElement>
//    {
//        private bool _mouseDown;

//        protected override void OnAttached()
//        {
//            AssociatedObject.MouseLeftButtonDown += AssociatedObject_MouseLeftButtonDown;
//            AssociatedObject.MouseMove += AssociatedObject_MouseMove;
//            AssociatedObject.MouseLeftButtonUp += AssociatedObject_MouseLeftButtonUp;
//        }



//        void AssociatedObject_MouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
//        {
//            _mouseDown = true;
           
//        }

//        void AssociatedObject_MouseMove(object sender, System.Windows.Input.MouseEventArgs e)
//        {
//            if (!_mouseDown) return;
//            (AssociatedObject.DataContext as MainViewModel).dragView.Execute(666); ;
//        }


//        void AssociatedObject_MouseLeftButtonUp(object sender, System.Windows.Input.MouseButtonEventArgs e)
//        {
//            _mouseDown = false;
//        }

//    }
//}
