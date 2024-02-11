import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';



@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  
  user = {
    username: '',
    email: '',
    password: '',
    password2: ''
  };
  
  constructor(private apiService: ApiService, private router: Router, private toastr: ToastrService) { }
  
  onsubmit() {
    
    this.apiService.register(this.user).subscribe(
      (data: any) => {
        console.log(data);
        this.toastr.success('Registered Successfully - Your request has been sent for approval !');
        this.router.navigate(['/login']) // Redirect to login
      },
      (error: any) => {
        console.error(error);
        if (error.status === 400 && error.error.email) {
          this.toastr.error("Invalid Email")
        } else {
          this.toastr.error("Please enter valid details !!!")
        }
      }
    );
    
  }
  emailPattern="[a-zA-Z0-9._%+-]+@\.gmail\.com"
  passwordPattern = /^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[A-Z]).{5,20}$/;

}
